from rest_framework import generics, status,permissions
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .serializers import UserRegistrationSerializer
from blogapp.models import User
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserLoginSerializer,BlogSerializer,AdminUserSerializer,CommentSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Blog, Comment
from django.http import HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError




def home(request):
    response = HttpResponse("Hello, Welcome to my Blog Page ", )
    return response


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email_subject = 'Welcome to our Blogging Platform'
        email_context = {
            'username': user.username,
        }
        email_html_message = render_to_string('mail.html', email_context)
        email_plain_message = strip_tags(email_html_message)  
        email = EmailMultiAlternatives(
            subject=email_subject,
            body=email_plain_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email],
        )
        email.attach_alternative(email_html_message, "text/html") 
        email.send()

        return Response('Registration successful. An email has been sent to your registered email address.', status=status.HTTP_201_CREATED)



class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    



class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
        subject = "Post Created"
        from_email = "mohammadshaheem593@gmail.com"
        to_email = [self.request.user.email]
        html_file_path = "templates/email_template.html"
        with open(html_file_path, "r") as html_file:
            html_content = html_file.read()
        html_content = html_content.replace("{{ Blog.title }}", instance.title)
        html_content = html_content.replace("{{ Blog.content }}", instance.content)
        if instance.image:
            html_content = html_content.replace("{{ Blog.image.url }}", instance.image.url)
        else:
            html_content = html_content.replace("{{ Blog.image }}", "")

        email = EmailMultiAlternatives(subject, "", from_email,to_email)
        email.attach_alternative(html_content, "text/html")
        if instance.image:
            try:
                email.attach_file(instance.image.path)
            except Exception as e:
                raise ValidationError("Error: " + str(e))

        try:
            email.send()
        except Exception as e:
            raise ValidationError("Error: " + str(e))

        return Response({"message": "Succesfully created"})

class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class AdminBlogPostList(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminBlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminCommentList(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminUserRegistrationView(generics.CreateAPIView):
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(is_staff=True, is_superuser=True)
