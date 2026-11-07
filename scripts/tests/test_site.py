"""Regression checks for release dates and workflow help destinations."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_site


class ReleaseCopyTests(unittest.TestCase):
    def test_next_release_date_reaches_all_documents(self):
        with patch.object(build_site, 'UPDATED', '2027-02-03'):
            for lang, label in [('en', 'Updated February 3, 2027'),
                                ('zh', '更新日期：2027 年 2 月 3 日')]:
                for page in ['support', 'privacy', 'terms']:
                    with self.subTest(lang=lang, page=page):
                        html = build_site.render(page, lang)
                        self.assertIn(f'<time datetime="2027-02-03">{label}</time>', html)
                        self.assertNotIn('November 7, 2026', html)

    def test_workflows_link_to_their_own_help(self):
        for lang in ['en', 'zh']:
            home = build_site.home(lang)
            support_route = build_site.route('support', lang)
            support = build_site.support(lang)
            for anchor in ['quick-start', 'listening', 'ssh']:
                with self.subTest(lang=lang, anchor=anchor):
                    self.assertEqual(home.count(f'href="{support_route}#{anchor}"'), 1)
                    self.assertIn(f'id="{anchor}"', support)


if __name__ == '__main__':
    unittest.main()
