
from .models import *
import time
from datetime import  timedelta
from celery import shared_task
from .views import scrape_indeed_jobs,scrape_and_save_jobs_technopark,Cyberpark_Jobs,Infopark_jobs
import logging

logger = logging.getLogger(__name__)


@shared_task
def test_task():
    try:
            minutes=120
            seconds = minutes * 60
            Infopark_jobs()
            Cyberpark_Jobs()
            scrape_and_save_jobs_technopark()
            scrape_indeed_jobs(job_name='python , data science , ml ,dl,flutter,mern,sql,testing,.net,django,technical support, webdeveloper,ai', location='Ernakulam', num_days=7)
            time.sleep(10)
            scrape_indeed_jobs(job_name='python , data science , ml ,dl,flutter,mern,sql,testing,.net,django,technical support, webdeveloper,ai', location='Kozhikode', num_days=7)
            time.sleep(10)
            scrape_indeed_jobs(job_name='python , data science , ml ,dl,flutter,mern,sql,testing,.net,django,technical support, webdeveloper,ai', location='Thiruvananthapuram', num_days=7)
            time.sleep(10)
            scrape_indeed_jobs(job_name='python , data science , ml ,dl,flutter,mern,sql,testing,.net,django,technical support, webdeveloper,ai', location='Kerala', num_days=7)
            time.sleep(10)
            scrape_indeed_jobs(job_name='developer , software engineer, frontend developer , backend developer ,restapi', location='Kerala', num_days=7)
            time.sleep(10)
            scrape_indeed_jobs(job_name='developer , software engineer, frontend developer , backend developer ,restapi', location='Ernakulam', num_days=7)
            time.sleep(10)
            scrape_indeed_jobs(job_name='react ,html,css ,Power bi,intern,Full stack developer ,restapi,junior ,software support,dart,', location='Kerala', num_days=7)
            time.sleep(10)
            scrape_indeed_jobs(job_name='python developer, python engineer, python programmer, python web developer, python software engineer,django developer', location='Kerala', num_days=7)
            time.sleep(10)
            scrape_indeed_jobs(job_name='django engineer, django web developer, django software engineer, django backend developer', location='Kerala', num_days=7)
            time.sleep(10)
            scrape_indeed_jobs(job_name='mern stack developer, mern developer, mongodb express react node developer, mern stack engineer, full stack mern developer', location='Kerala', num_days=7)
            time.sleep(10)
            scrape_indeed_jobs(job_name='mean stack developer, mean developer, mongodb express angular node developer, mean stack engineer, full stack mean developer', location='Kerala', num_days=7)
            time.sleep(10)
            scrape_indeed_jobs(job_name='software tester, qa engineer, quality assurance analyst, manual tester, automation tester', location='Kerala', num_days=7)
            time.sleep(10)
            scrape_indeed_jobs(job_name='java developer, java engineer, java programmer, java software engineer, java web developer', location='Kerala', num_days=7)
            time.sleep(10)
            scrape_indeed_jobs(job_name='.net developer, .net engineer, .net programmer, .net software engineer, .net web developer', location='Kerala', num_days=7)
            time.sleep(10)
            scrape_indeed_jobs(job_name='data scientist, data analyst, data engineer, machine learning engineer, data science specialist,Mobile Application Developer', location='Kerala', num_days=7)
            time.sleep(10)
            scrape_indeed_jobs(job_name='flutter developer, flutter engineer, flutter mobile developer, flutter app developer, flutter software engineer,"Analyst', location='Kerala', num_days=7)
            print("completed")
            time.sleep(seconds)
            
            indeed_deletion_date = timezone.now() - timedelta(days=7)
            IndeedJobs.objects.filter(datetime__lte=indeed_deletion_date).delete()
            print("Indeed Cleared")
            technopark_deletion_date = timezone.now()
            TechnoparkJobs.objects.filter(closing_date__lt=technopark_deletion_date).delete()
            print("TechnoPark Jobs Cleared")
            cyberpark_deletion_date = timezone.now()-timedelta(days=20)
            CyberparkJobs.objects.filter(datetime__lte=cyberpark_deletion_date).delete()
            print("TechnoPark Jobs Cleared")
            pass
    except Exception as e:
        logger.error("An error occurred: %s", e, exc_info=True)



        
    
# @shared_task
# def test_task():
#     print("Task is running")
#     
#     return "Task Completed"


