from django.conf import settings

from agent.services.subscribe import create_unsubscribe_link_token


def generate_unsub_link(user):

    email, token = create_unsubscribe_link_token(user.email)
    return (
        '<br><br><br><br><br><br><br><br>'
        '<small><i style="font-weight: lighter; color: #aaaaaa">'
        'If you no longer wish to receive these emails, please click '
        f'<a href="{settings.FRONTEND_BASE_URL}unsubscribe?email={email}&unsubscribe_token={token}">Unsubscribe</a>.</i></small>'  # noqa
    )


def generate_delivery_email_content(giver, receiver, link):
    return f"""
        Dear {receiver.user.first_name},<br>
        <p>Exciting news –  {giver.user.first_name} {giver.user.last_name} has gifted you something truly special: Agent! It's a heartfelt service designed to bring joy to your everyday life. Imagine receiving daily check-in calls from a friendly companion who’ll be checking your well-being and eager to hear about your day .</p>
        <p>With Agent, there’s no tech setup required. You’ll get a daily call to chat, laugh, and stay connected.</p>
        <p>Ready to start this delightful journey? Just click this link <a href={link}>{link}</a> to schedule your first call. We can’t wait to brighten your day!</p>

        Warm regards,<br>
        The Agent Team<br>

        {generate_unsub_link(receiver.user)}
    """  # noqa


def generate_delivery_email_content_for_themselves(giver, receiver, link, message):
    # Replace newline characters in the message with <br> tags for HTML formatting
    formatted_message = message.replace('\n', '<br>')
    return f"""
        Dear {receiver.user.first_name},<br>
        <p>With Agent, there's no need for any tech setup. You'll get a weekly call to share and record your memories. It’s all about celebrating your life and keeping your mind active and joyful.</p>
        <p>Ready to kickstart this journey? Just click this link <a href={link}>{link}</a> to schedule your first weekly chat. We're excited to hear your stories!</p>

        Warm regards,<br>
        The Agent Team<br>

        {generate_unsub_link(receiver.user)}
    """  # noqa


def generate_reset_password_email_content(user, reset_pwd_link):
    return (
        '<b>It seems like you forgot your password.</b>'
        '<p>No worries! Just click the link below, and you will be able to change it safely!</p>'
        f'<p><a href={reset_pwd_link}> Reset Password</a><br>If you did not make this request, please ignore this email.<br></p>'  # noqa
        'Thanks,<br>The Agent Team'
        f'{generate_unsub_link(user)}'
    )


def generate_welcome_email_content(user, url, token):
    if user.self_gift:
        return (
            f'<p>Hi {user.first_name if user.first_name else "there"}!</p>'
            f"<p>Welcome aboard! 🎉 We're glad you're with us. First things first, let’s get you set up. Please create your password <a href={url}?token={token}>here</a>.</p>"
            "<p>At Agent, we make daily calls to you to check in and catch up, like a good friend. We're excited to have you and can’t wait to make every day a little brighter for you!</p>"
            "Cheers,<br>The Agent Team"
            f'{generate_unsub_link(user)}'
        )
    else:
        return (
            f'<p>Hi {user.first_name if user.first_name else "there"}!</p>'
            f"<p>Welcome aboard! 🎉 We're glad you're with us. First things first, let’s get you set up. Please create your password <a href={url}?token={token}>here</a>.</p>"
            "<p>At Agent, we make daily calls to your loved ones to catch up, cheer them up, and just check in, like a good friend. No apps, no hassle—just chats that brighten their day and keep you in the loop right after.</p>"
            "<p>We're excited to have you and can’t wait to make every day a little brighter for your family!</p>"
            "Cheers,<br>The Agent Team"
            f'{generate_unsub_link(user)}'
        )


def generate_invitation_email_to_user_from_receiver_content(user, link, receiver, daily_update):
    if daily_update:
        return (
            f'<p>Hey {user.first_name if user.first_name else "there"},</p>'
            f"<p>{receiver.user.first_name} {receiver.user.last_name} thought it would be wonderful for you to stay connected to their daily life. Now you’ll receive updates about {receiver.user.first_name} {receiver.user.last_name} every day.</p>"
            "Cheers,<br>The Agent Team"
            f'{generate_unsub_link(user)}'
        )
    else:
        return (
            f'<p>Hey {user.first_name if user.first_name else "there"},</p>'
            f"<p>{receiver.user.first_name} {receiver.user.last_name} thought it would be wonderful for you to be one of their designated contacts. You will receive notifications if we are unable to make contact with {receiver.user.first_name} {receiver.user.last_name} during our regular check-ins.</p>"
            "Cheers,<br>The Agent Team"
            f'{generate_unsub_link(user)}'
        )


def generate_invitation_email_to_user_from_giver_content(user, link, giver, receiver, daily_update):
    if daily_update:
        return (
            f'<p>Hey {user.first_name if user.first_name else "there"},</p>'
            f"<p>{giver.user.first_name} {giver.user.last_name} thought it would be wonderful for you to stay connected to {receiver.user.first_name} {receiver.user.last_name}'s daily life. Now you’ll receive updates about {receiver.user.first_name} {receiver.user.last_name} every day.</p>"
            "Cheers,<br>The Agent Team"
            f'{generate_unsub_link(user)}'
        )
    else:
        return (
            f'<p>Hey {user.first_name if user.first_name else "there"},</p>'
            f"<p>{giver.user.first_name} {giver.user.last_name} thought it would be wonderful for you to be one of {receiver.user.first_name} {receiver.user.last_name}'s designated contacts. You will receive notifications if we are unable to make contact with {receiver.user.first_name} {receiver.user.last_name} during our regular check-ins.</p>"
            "Cheers,<br>The Agent Team"
            f'{generate_unsub_link(user)}'
        )

def generate_invitation_email_to_non_user_from_receiver_content(link, receiver, daily_update):
    if daily_update:
        return (
            f'<p>Hey there,</p>'
            f"<p>{receiver.user.first_name} {receiver.user.last_name} has invited you to join Agent, where you can stay connected to their daily life. Agent is a unique service where individuals like {receiver.user.first_name} {receiver.user.last_name} receive daily check-in calls from our companions, sharing updates and stories from their day.<br></p>"
            f"<p>{receiver.user.first_name} {receiver.user.last_name} thought it would be wonderful for you to receive these updates. To accept, just click <a href={link}>here</a>.</p>"
            "Cheers,<br>The Agent Team"
        )
    else:
        return (
            f'<p>Hey there,</p>'
            f"<p>{receiver.user.first_name} {receiver.user.last_name} has invited you to receive important updates about them through Agent, a daily companionship and check-in service. As part of this new arrangement, you will receive notifications if we are unable to make contact with {receiver.user.first_name} {receiver.user.last_name} during our regular check-ins.<br></p>"
            f'<p>You also have the option to receive a daily update about {receiver.user.first_name} {receiver.user.last_name}, keeping you informed and connected.<br></p>'
            f"<p>To accept, just click <a href={link}>here</a>.</p>"
            "Cheers,<br>The Agent Team"
        )


def generate_invitation_email_to_non_user_from_giver_content(link, giver, receiver, daily_update):
    if daily_update:
        return (
            f'<p>Hey there,</p>'
            f"<p>{giver.user.first_name} {giver.user.last_name} has invited you to join Agent, where you can stay connected to {receiver.user.first_name} {receiver.user.last_name}'s daily life. Agent is a unique service where individuals like {receiver.user.first_name} {receiver.user.last_name} receive daily check-in calls from our companions, sharing updates and stories from their day.<br></p>"
            f"<p>{giver.user.first_name} {giver.user.last_name} thought it would be wonderful for you to receive these updates.To accept, just click <a href={link}>here</a>.</p>"
            "Cheers,<br>The Agent Team"
        )
    else:
        return (
            f'<p>Hey there,</p>'
            f"<p>{giver.user.first_name} {giver.user.last_name} has invited you to receive important updates through Agent, a daily companionship and check-in service for {receiver.user.first_name} {receiver.user.last_name}. As part of this new arrangement, you will receive notifications if we are unable to make contact with {receiver.user.first_name} {receiver.user.last_name} during our regular check-ins.<br></p>"
            f"<p>You also have the option to receive a daily update about {receiver.user.first_name} {receiver.user.last_name}, keeping you informed and connected.<br></p>"
            f"<p>To accept, just click <a href={link}>here</a>.</p>"
            "Cheers,<br>The Agent Team"
        )


def generate_abandoned_cart_email_content(user, link):
    if user.self_gift:

        return f"""
            Hey {user.first_name if user.first_name else "there"}!<br>
            <p>Looks like you're just one step away from enriching your own daily routine. Ready to make it happen? Here’s your link to finish up: <a href={link}>{link}</a></p>
    
            <p>With Agent, you’ll enjoy a friendly daily call from our companion, and we’ll keep your designated contacts updated on your well-being. </p>
            
            <p>If you have any questions or need assistance, we’re here for you!</p>
            
            Cheers,<br>
            The Agent Team<br>
    
            {generate_unsub_link(user)}
        """  # noqa
    else:
        return f"""
                Hey {user.first_name if user.first_name else "there"}!<br>
                <p>Looks like you're just one step away from bringing daily smiles to your loved ones. Ready to make it happen? Here's your link to finish up: <a href={link}>{link}</a></p>

                <p>With Agent, not only do your elders receive a friendly daily call from our companion, but you'll also get immediate updates after each chat. It’s a perfect way to stay connected and ensure they’re not just okay, but happy and engaged.</p>

                <p>If you have any questions or need assistance, we’re here for you!</p>

                Cheers,<br>
                The Agent Team<br>

                {generate_unsub_link(user)}
            """  # noqa


def generate_gift_sent_email_content(giver, receiver):

    return f"""
        Hi {giver.user.first_name if giver.user.first_name else "there"},<br>
        <p>We're excited to let you know that your special Agent gift message has been successfully delivered to {receiver.user.first_name} at their email: {receiver.user.email}.</p>

        <p>To enhance their experience, <b>we suggest reaching out to {receiver.user.first_name} for a personal touch.</b> It’s a great opportunity to: <br></p>
        <ul>
            <li>Share your personal reasons for choosing Agent as a gift. Let them know how much their well-being means to you.</li>
            <li>Explain what they can expect next.</li>
        </ul>

        <p>This personal touch can really set the stage for a wonderful Agent journey.</p>
        
        <p>Thanks for bringing Agent into your loved one’s life!</p>
        
        Warm regards,<br>
        The Agent Team<br>

        {generate_unsub_link(giver.user)}
    """  # noqa


def generate_story_shared_email_content(giver, receiver, message):
    # Replace newline characters in the message with <br> tags for HTML formatting
    formatted_message = message.replace('\n', '<br>')

    return f"""
        Hi {giver.user.first_name if giver.user.first_name else "there"},<br> 
        <p>Here is today's update on {receiver.user.first_name}.<br></p>
        <p>{formatted_message}</p>
        {generate_unsub_link(giver.user)}
    """  # noqa


def generate_reminder_email_content(giver, receiver, number):

    return f"""
        Hi {giver.user.first_name if giver.user.first_name else "there"},<br>
        
        <p>We tried reaching {receiver.user.first_name} several times today but couldn't get through. It might be a good idea to check in with them to see if everything is okay.</p>
        
        Best,<br>
        The Agent Team<br>
        {generate_unsub_link(giver.user)}
    """  # noqa


def generate_reminder_email_to_receiver_content(receiver, number):

    return f"""
        <p>Hey {receiver.user.first_name if receiver.user.first_name else ""}, it's Ethan from Agent. We missed chatting with you these past few weeks about your life stories and just want to make sure everything's alright. Can you give us a call back at {number}? Looking forward to catching up!</p>

        {generate_unsub_link(receiver.user)}
    """  # noqa


def generate_schedule_reminder_email_to_giver_content(giver, receiver):

    return f"""
        Hello! Just a heads up, we sent the Agent gift message to {receiver.user.first_name} yesterday. However, {receiver.user.first_name} hasn't set up their daily call time yet. Could you kindly remind them to schedule it as soon as possible using the link we sent? Appreciate it!
        {generate_unsub_link(giver.user)}
    """  # noqa


def generate_schedule_reminder_email_to_receiver_content(giver, receiver, link):
    return f"""
            Hello! Just a reminder to schedule your daily Agent call using this link <a href={link}>{link}</a>. It would be great to have this organized so you can fully benefit from our service.
            {generate_unsub_link(receiver.user)}
            """  # noqa


def generate_story_shared_text_content(giver, receiver, message):
    return (
        f"""
        Hi {giver.user.first_name if giver.user.first_name else "there"}, 
        
        Here is today's update on {receiver.user.first_name}. 
        
        {message}
        """
    )
