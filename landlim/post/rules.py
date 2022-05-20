from .models import AccessLevelChoice
import rules

@rules.predicate
def has_access_permission(user, post):
    if post.access_level == AccessLevelChoice.private.name:
        if post.user != user:
            return False
    return True
rules.add_perm('post.can_access', has_access_permission)