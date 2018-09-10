


def recurring_event_handler(event, context):
    print("**** RecurringEvents.recurring_event_handler")
    my_kwargs = event.get('kwargs')
    print(f"***** kwargs: {my_kwargs}")

    return 'Done'


def every_2_mins(event, context):
    print("**** RecurringEvents.every_2_mins")
    my_kwargs = event.get('kwargs')
    print(f"***** kwargs: {my_kwargs}")

    return 'Done'
