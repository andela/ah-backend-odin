from django.shortcuts import render, get_object_or_404

from rest_framework import status
from rest_framework.permissions import  IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import ReporterJsonRenderer
from .serializers import ReportedArticleSerializer
from .models import ReportArticle
from django.conf import settings
from django.core.mail import send_mail

from ..articles.models import Article
from ..authentication.models import User
from ..authentication.backends import JWTAuthentication


class ReportingAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ReporterJsonRenderer,)
    serializer_class = ReportedArticleSerializer

    def post(self, request, slug):

        user_info = JWTAuthentication().authenticate(request)
        
        report = request.data.get('report', {})
        article = Article.objects.get(slug=slug)

        report['user'] = user_info[0].pk
        report['article'] = article.id
        reason = report['reason']

        serializer = self.serializer_class(data=report)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        reporter_username = User.objects.get(id=article.author_id).username

        mail_subject = 'REPORTER: {} has reported an article .'.format(reporter_username)
        domain = settings.BASE_URL
        email = 'authorshaventia@gmail.com'

        template = '''Greetings Admin,

        Please note that the above mentioned user has reported the article below:
        {}/api/articles/{}

        Reason: {}

        '''.format(domain, slug, reason)


        send_mail(mail_subject, template, email, [email])

        return Response(serializer.data, status=status.HTTP_201_CREATED)

