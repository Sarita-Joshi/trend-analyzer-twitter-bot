from src.poller.poll_generator import PollGenerator

def test_generate_poll():
    pg = PollGenerator()
    text = "EV budget cut by $500k. Tesla stock drops."
    poll = pg.generate(text)
    assert isinstance(poll, dict)
    assert "question" in poll and "options" in poll
    assert len(poll['options']) > 1