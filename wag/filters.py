from templates import jinja_env
from datetime import datetime, timedelta
import html2text

def html_to_markdown(value, width=70):
    html2text.BODY_WIDTH = width
    return html2text.html2text(value)

def relatize(value, feed_timezone=-8, time_format="%Y-%m-%dT%H:%M:%S-08:00"):
    """
    
    Returns the relative time of each request.  Another feature stolen from
    github.

    time_format - the format of your time.  everything should make sense
                  except the -08:00.  The -08:00 is the time zone.  The
                  timezone may put into its own variable at a later date.
    
    feed_time_zone - is the timezone of the feed

    How it works:
    
        get the date from value and time_format
        subtract current timezone to get utc time
        
        get current utc time.
        compare current utc time and output relative time
        
    """
    
    the_date = datetime.strptime(value, time_format)
    utc_date = the_date - timedelta(hours=feed_timezone)
    
    now = datetime.utcnow()

    time_difference = now - utc_date
    
    if time_difference.days > 356:
        return 'about %d years ago' % (time_difference.days / 356)
    elif time_difference.days > 1:
        return 'about %d days ago' % time_difference.days
    elif time_difference.days > 0:
        return 'about a day ago'
    elif time_difference.seconds > 7200:
        return 'about %d hours ago' % (time_difference.seconds / 3600)
    elif time_difference.seconds > 3600:
        return 'about an hour ago'
    elif time_difference.seconds > 120:
        return 'about %d minutes ago' % (time_difference.seconds / 60)
    elif time_difference.seconds > 60:
        return 'about a minute ago'
    elif time_difference.seconds < 60:
        return 'just now'
    
jinja_env.filters['html2markdown'] = html_to_markdown
jinja_env.filters['relatize'] = relatize