from buckstats.app import db
import buckstats.model as m

##TODO this is confusing and should be put into a class
## also the name sucks


def get_last_event_in(events):
    return db.session.query(m.Event)\
        .filter(m.Event.event.in_(events))\
        .order_by(m.Event.time.desc())\
        .first()


def get_last_lock_event():
    return get_last_event_in(['unlocked', 'locked'])


def get_last_position_event():
    return get_last_event_in(['sitting', 'standing'])


def get_last_derived_position():
    return db.session.query(m.DerivedPosition)\
        .order_by(m.DerivedPosition.start_time.desc())\
        .first()


def add_new_status(position, time):
    new_status = m.DerivedPosition(position=position, start_time=time)
    db.session.add(new_status)


def position_changed(event):
    last_lock_event = get_last_lock_event()
    assert(last_lock_event)

    # Since this function received a sitting or standing event,
    # we only need to take action if the computer is unlocked.
    # If the computer is locked, any previous sitting/standing events
    # would have been closed and no stand status needs to be created.

    if last_lock_event.event == 'unlocked':
        last_position = get_last_derived_position()

        if last_position and last_position.position != event.event:
            # If this event matches the previous status's position, then
            # it essentially means a duplicate sitting/standing event
            # was created. Only make changes if that is not the case.
            last_position.end_time = event.time
            add_new_status(event.event, event.time)

        elif not last_position:
            add_new_status(event.event, event.time)


def lock_changed(event):
    if event.event == 'unlocked':
        last_position_event = get_last_position_event()
        position = last_position_event.event if last_position_event else 'sitting'
        add_new_status(position, event.time)

    elif event.event == 'locked':
        last_position = get_last_derived_position()
        assert(last_position and not last_position.end_time)
        last_position.end_time = event.time


def event_created(event):
    if event.event in ('sitting', 'standing',):
        position_changed(event)

    elif event.event in ('unlocked', 'locked',):
        lock_changed(event)

    else:
        assert(False)

    db.session.commit()
