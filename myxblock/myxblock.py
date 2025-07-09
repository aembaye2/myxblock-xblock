import random
from importlib.resources import files

from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Integer, Float, Scope
from xblock.fragment import Fragment
# from xblock.runtime import StudioEditableXBlockMixin


class MyXBlock(XBlock):
    """
    A simple math problem XBlock that allows num1 and num2 to be set in Studio.
    """

    # Content-scoped fields for author editing in Studio
    num1 = Integer(default=5, scope=Scope.content, help="First number")
    num2 = Integer(default=7, scope=Scope.content, help="Second number")

    # Student-specific fields
    score = Float(default=0, scope=Scope.user_state)
    question = Integer(default=0, scope=Scope.user_state)

    def resource_string(self, path):
        return files(__package__).joinpath(path).read_text(encoding="utf-8")

    def student_view(self, context=None):
        """
        Student view: displays the question and input box.
        """
        html = self.resource_string("static/html/myxblock.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/myxblock.css"))
        frag.add_javascript(self.resource_string("static/js/src/myxblock.js"))
        frag.initialize_js('MyXBlock')
        return frag

    @XBlock.json_handler
    def submit_answer(self, data, suffix=''):
        answer = int(data.get('answer', 0))
        correct_answer = self.num1 + self.num2

        self.score = 1 if answer == correct_answer else 0
        self.runtime.publish(
            self, 'grade', {'value': self.score, 'max_value': 1})
        return {'score': self.score, 'correct_answer': correct_answer}

    def studio_view(self, context=None):
        """
        View shown to course authors in Studio for editing num1 and num2.
        """
        html = f"""
        <div>
            <label>First Number (num1):</label>
            <input type="number" name="num1" value="{self.num1}" /><br/><br/>

            <label>Second Number (num2):</label>
            <input type="number" name="num2" value="{self.num2}" /><br/><br/>

            <input class="save-button" type="button" value="Save"/>
        </div>
        """
        frag = Fragment(html)
        frag.add_javascript("""
            function MyXBlockStudio(runtime, element) {
                $('.save-button', element).click(function() {
                    var num1 = $('input[name=num1]', element).val();
                    var num2 = $('input[name=num2]', element).val();
                    runtime.notify('save', {state: 'start'});
                    runtime.xblock(element).save_settings({
                    num1: parseInt(num1),
                    num2: parseInt(num2)
            }).done(function() {
                        runtime.notify('save', {state: 'end'});
                    }).fail(function() {
                        runtime.notify('error', {
                            msg: "Save failed."
                        });
                    });
                });
            }
        """)
        frag.initialize_js('MyXBlockStudio')
        return frag

    def save(self):
        """
        Not required for JSON-based saving.
        """
        pass

    def get_content(self):
        return f"{self.num1} + {self.num2} = ?"

    @XBlock.json_handler
    def save_settings(self, data, suffix=''):
        """
        JSON handler to save Studio-edited fields.
        """
        self.num1 = int(data.get('num1', 0))
        self.num2 = int(data.get('num2', 0))
        return {"result": "success"}

    @staticmethod
    def workbench_scenarios():
        return [
            ("MyXBlock",
             """<myxblock/>"""),
        ]
