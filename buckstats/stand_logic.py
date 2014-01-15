from buckstats.app import db
import buckstats.model as m

##TODO this is confusing and should be put into a class
## also the name sucks

STARTUP = 'startup'
SHUTDOWN = 'shutdown'
UNLOCKED = 'unlocked'
LOCKED = 'locked'
SITTING = 'sitting'
STANDING = 'standing'


def get_last_event_in(events):
    return db.session.query(m.Event)\
        .filter(m.Event.event.in_(events))\
        .order_by(m.Event.time.desc())\
        .first()


def get_last_computer_event():
    return get_last_event_in([STARTUP, SHUTDOWN, UNLOCKED, LOCKED])


def get_last_position_event():
    return get_last_event_in([SITTING, STANDING])


def get_last_derived_position():
    return db.session.query(m.DerivedPosition)\
        .order_by(m.DerivedPosition.start_time.desc())\
        .first()


def add_new_status(position, time):
    new_status = m.DerivedPosition(position=position, start_time=time)
    db.session.add(new_status)


def position_changed(event):
    last_comp_event = get_last_computer_event()
    assert(last_comp_event)

    # Since this function received a sitting or standing event,
    # we only need to take action if the computer is unlocked.
    # If the computer is locked, any previous sitting/standing events
    # would have been closed and no stand status needs to be created.

    if last_comp_event.event in (STARTUP, UNLOCKED,):
        last_position = get_last_derived_position()

        if last_position and last_position.position != event.event:
            # If this event matches the previous status's position, then
            # it essentially means a duplicate sitting/standing event
            # was created. Only make changes if that is not the case.
            last_position.end_time = event.time
            add_new_status(event.event, event.time)

        elif not last_position:
            add_new_status(event.event, event.time)


def computer_changed(event):
    if event.event in (STARTUP, UNLOCKED,):
        last_position_event = get_last_position_event()
        position = last_position_event.event if last_position_event else SITTING
        add_new_status(position, event.time)

    elif event.event in (SHUTDOWN, LOCKED,):
        last_position = get_last_derived_position()
        assert(last_position and not last_position.end_time)
        last_position.end_time = event.time


def event_created(event):
    if event.event in (SITTING, STANDING,):
        position_changed(event)

    else:
        computer_changed(event)

    db.session.commit()
