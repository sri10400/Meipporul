class InterviewSession:
    def __init__(self, session_id, candidate, profile):
        self.session_id = session_id
        self.candidate = candidate
        self.profile = profile

        self.questions = []
        self.answers = []
        self.topics_covered = []

        self.current_question = None
        self.question_count = 0

        self.scores = {}

        self.done = False


class SessionManager:
    def __init__(self):
        self.sessions = {}

    def create_session(self, session_id, candidate, profile):
        session = InterviewSession(
            session_id=session_id,
            candidate=candidate,
            profile=profile
        )

        self.sessions[session_id] = session

        return session

    def get_session(self, session_id):
        return self.sessions.get(session_id)

    def delete_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]

    def session_exists(self, session_id):
        return session_id in self.sessions