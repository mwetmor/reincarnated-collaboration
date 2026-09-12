from review.build_review import build_review
from gates_helpers import *
class Tests(TemporaryTest):
    def test_template_and_invalid_atlas(self):
        out=self.base/'review.html'
        build_review({'animations':{},'available_frames':0},{'modules':{}},{},out)
        text=out.read_text();self.assertNotIn('__ASSET_DATA__',text);self.assertIn('function combinedState(t)',text)
        with self.assertRaises(ValueError):build_review({}, {}, {}, out)

    def test_script_injection_is_escaped(self):
        out=self.base/'review.html'
        build_review({'animations':{},'available_frames':0,'note':'</script><script>bad()'},{'modules':{}},{},out)
        self.assertNotIn('</script><script>bad()',out.read_text())
        self.assertIn(r'\u003c/script>',out.read_text())
