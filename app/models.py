from django.conf import settings
from django.db import models

from django.utils import timezone                                   # model field ma timestamp type chaina vayera timezone lai import gareko
from django.utils.text import slugify                               # slugify is built in feature in django

# signals imports
from django.dispatch import receiver                                # receiver decorator use garnu parne vayeko le receiver lai import gareko

from django.db.models.signals import (
    pre_save,                                                       # jasto khalko inbuilt model signals haru chaincha tini haru sabailai import gareko
    post_save,
    pre_delete,
    post_delete,
    m2m_changed,
)

User = settings.AUTH_USER_MODEL                                     # By default settings.AUTH_USER_MODEL vaneko, django le diyeko authentication user model ... we can overwrite settings.AUTH_USER_MODEL in settings.py to create custom user model for us


# signals ko code haru dherai jaso models.py file vitrai lekhincha


# FOR PRE SAVE
# Best Way(one way) using receiver decorator:
# @receiver(pre_save, sender=User)                                  # sender ma model class ko name aaucha
# def user_pre_save_receiver(sender, instance, *args, **kwargs):    # NOte: pre_save doesn't have created argument # yo line ko instance le sender ma vayeko model class ma vayeko instance or object lai refer garcha
#     """
#     before saved in the database
#     """
#     print("--PRE SAVE RUNNING--")

#     print(instance.username, instance.id) # None

#     # instance.save()   <- Never do this inside pre_save,, because this satement create infinte recurssion (infinite loop)
    

#Another Way(2nd way):
# pre_save.connect(user_created_handler, sender=User)



# FOR POST SAVE
# Best Way:
# @receiver(post_save, sender=User)                                 # sender ma model class ko name aaucha
# def user_post_save_receiver(sender, instance, created, *args, **kwargs):    # post_save has created argument  # yo line ko instance le sender ma vayeko model class ma vayeko instance or object lai refer garcha
#     """
#     after saved in the database
#     """
#     print("--POST SAVE RUNNING--")

#     if created:
#         print("Send email to", instance.username)

#         # trigger pre_save
#         # instance.save()                                         # you can do this in post_save if you wanto to save again... yo statement le feri ek choti pre_save & post_save run garaucha
#         # trigger post_save
#     else:
#         print("Updating Record of", instance.username)

# Another Way:
# # post_save.connect(user_created_handler, sender=User)





# Creating BlogPost model
class BlogPost(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True)
    liked = models.ManyToManyField(User, blank=True)
    notify_users = models.BooleanField(default=False)
    notify_users_timestamp = models.DateTimeField(blank=True, null=True, auto_now_add=False)
    active = models.BooleanField(default=True)


# Using PRE SAVE
# @receiver(pre_save, sender=BlogPost)                              # sender ko naam model class ko name lekhincha... instance refers to this sender
# def blog_post_pre_save(sender, instance, *args, **kwargs):        # yo line ko instance le sender ma vayeko model class ma vayeko instance or object lai refer garcha
#     if not instance.slug:
#         instance.slug = slugify(instance.title)                   # django le diyeko slugify() feature use garera title lai slug ma convert gareko cha .. example: hello dhiraj  ==> hello-dhiraj


# Using POST SAVE
# @receiver(post_save, sender=BlogPost)                             # sender ko naam model class ko name lekhincha.
# def blog_post_post_save(sender, instance, created, *args, **kwargs):      # note yaha created argument huncha # # yo line ko instance le sender ma vayeko model class ma vayeko instance or object lai refer garcha
#     if instance.notify_users:                                     # yedi notify_users field ko value True cha vani matra yo if condition vitra ko execute hune
#         print("notify users")
#         instance.notify_users = False                             # aba chai notify_users field ko value lai False garayeko
#         # celery worker task -> offload -> Time & Tasks 2 cfe.sh
#         instance.notify_users_timestamp = timezone.now()
#         instance.save()                                           # object ko fields haru ko value ma changer gari sake pachi chai object lai feri save() tw garna pari nai halcha



# Using PRE DELETE
# @receiver(pre_delete, sender=BlogPost)
# def blog_post_pre_delete(sender, instance, *args, **kwargs):
#     # move or make a backup of this data
#     print(f"{instance.id} will be removed")

# # pre_delete.connect(blog_post_pre_delete, sender=BlogPost)



# Using POST DELETE
# @receiver(post_delete, sender=BlogPost)
# def blog_post_post_delete(sender, instance, *args, **kwargs):
#     #  celery worker task -> offload -> Time & Tasks 2 cfe.sh
#     print(f"{instance.id} has been removed")

# # post_delete.connect(blog_post_post_delete, sender=BlogPost)



# Using Many To Many signal
# @receiver(m2m_changed, sender=BlogPost.liked.through)           # BlogPost.liked.trhough vannale BlogPost vanni model ko liked vanni field ko value ma kei change vayo vani 
# def blog_post_liked_changed(sender, instance, action, *args, **kwargs):

#     print(args, kwargs)
#     print(action)

#     if action == 'pre_add':
#         print("was added")
#         qs = kwargs.get("model").objects.filter(pk__in=kwargs.get('pk_set'))
#         print(qs.count())
