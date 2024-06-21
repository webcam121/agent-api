from django.urls import path

from agent.apps.accounts.views import ListGiftReceiverView, DetailGiftReceiverView, \
    UpdateReceiver, TrialDetailGiftReceiverByPhoneNumberView, \
    RetrieveGiverDetailForReceiverView, \
    RegisterPreGiftReceiverView, DetailPreGiftReceiverView, UpdatePreReceiver, RetrieveMostRecentPreReceiver, \
    InviteUserForReceiverView, InviteUserForGiverView, AcceptInvitationTokenView, \
    DetailPreReceiverByGiverPhoneNumberView, DetailPaidGiverByReceiverPhoneNumberView, InviteUserForReceiverView, \
    InviteUserForGiverView, AcceptInvitationTokenView, ListPreReceiverView, \
    TestNotificationView, SkipTriviaGameView, DetailCallerPhoneNumberView, DailyUpdateModifyForGiverView, \
    DailyUpdateModifyForReceiverView

app_name = 'gift_receivers'

urlpatterns = [
    path('', ListGiftReceiverView.as_view()),
    path('trial_phone_number/<str:phone_number>/', TrialDetailGiftReceiverByPhoneNumberView.as_view()),
    # Script API to get pre_receiver name for a gift giver
    path('phone_number/<str:phone_number>/pre_receiver/', DetailPreReceiverByGiverPhoneNumberView.as_view()),
    path('phone_number/<str:phone_number>/paid_giver/', DetailPaidGiverByReceiverPhoneNumberView.as_view()),
    path('trivia_game/reset/<str:phone_number>/', SkipTriviaGameView.as_view()),
    # Disable this one since all registered receivers are pre-receivers
    # path('register/', RegisterGiftReceiverView.as_view()),
    path('receivers/<int:pk>/', DetailGiftReceiverView.as_view()),
    # path('receivers/<int:pk>/update/', UpdateReceiver.as_view()),
    path('giver/', RetrieveGiverDetailForReceiverView.as_view()),
    # for pre receivers
    path('pre_receivers/', ListPreReceiverView.as_view()),
    path('pre_receivers/register/', RegisterPreGiftReceiverView.as_view()),
    path('pre_receivers/latest/', RetrieveMostRecentPreReceiver.as_view()),
    path('pre_receivers/<int:pk>/', DetailPreGiftReceiverView.as_view()),
    path('pre_receivers/<int:pk>/update/', UpdatePreReceiver.as_view()),
    # Invitation
    path('invite/', InviteUserForReceiverView.as_view()),
    path('invite/<int:receiver_id>/', InviteUserForGiverView.as_view()),
    path('accept_invitation/', AcceptInvitationTokenView.as_view()),
    # daily_update
    path('daily_update/givers/<int:gift_receiver_id>/', DailyUpdateModifyForGiverView.as_view()),
    path('daily_update/receivers/<int:gift_giver_id>/', DailyUpdateModifyForReceiverView.as_view()),

    path('test/', TestNotificationView.as_view())
]
