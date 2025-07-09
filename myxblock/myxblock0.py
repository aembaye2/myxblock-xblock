"""A simple math problem XBlock."""

import random
from importlib.resources import files

from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Integer, Float, Scope


class MyXBlock(XBlock):
    """
    A simple math problem XBlock.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.
    score = Float(default=0, scope=Scope.user_state)
    num1 = Integer(default=0, scope=Scope.user_state)
    num2 = Integer(default=0, scope=Scope.user_state)
    question = Integer(default=0, scope=Scope.user_state)

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        return files(__package__).joinpath(path).read_text(encoding="utf-8")

    def student_view(self, context=None):
        """
        The primary view of the MyXBlock, shown to students
        when viewing courses.
        """
        if self.question == 0:
            self.num1 = random.randint(1, 100)
            self.num2 = random.randint(1, 100)
            self.question = 1

        html = self.resource_string("static/html/myxblock.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/myxblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/myxblock.js"))
        frag.initialize_js('MyXBlock')
        return frag

    @XBlock.json_handler
    def submit_answer(self, data, suffix=''):
        """
        Checks the answer, updates the score, and publishes the grade.
        """
        answer = int(data.get('answer', 0))
        correct_answer = self.num1 + self.num2

        if answer == correct_answer:
            self.score = 1
        else:
            self.score = 0

        self.question = 0

        self.runtime.publish(
            self, 'grade', {'value': self.score, 'max_value': 1})

        return {'score': self.score, 'correct_answer': correct_answer}

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("MyXBlock",
             """<myxblock/>
             """),
            ("Multiple MyXBlock",
             """<vertical_demo>
                <myxblock/>
                <myxblock/>
                <myxblock/>
                </vertical_demo>
             """),
        ]
