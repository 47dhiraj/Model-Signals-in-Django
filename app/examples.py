from django.contrib.auth import get_user_model

User = get_user_model()



# pre_save -> instance  -> receiver function
instance = User.objects.create() # save User data in the database
# post_save -> instance, created=True -> receiver function

# pre_save -> instance  -> receiver function
instance.save()
# post_save -> instance, created=False  -> receiver function

# pre_delete -> instance  -> receiver function
instance.delete()
# post_delete -> instance  -> receiver function