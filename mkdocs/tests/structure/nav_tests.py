#!/usr/bin/env python

import sys
import unittest

from mkdocs.structure.nav import get_navigation
from mkdocs.structure.files import File, Files
from mkdocs.structure.pages import Page
from mkdocs.tests.base import dedent, load_config


class SiteNavigationTests(unittest.TestCase):

    maxDiff = None

    def test_simple_nav(self):
        nav_cfg = [
            {'Home': 'index.md'},
            {'About': 'about.md'}
        ]
        expected = dedent("""
        Page(title='Home', url='/')
        Page(title='About', url='/about/')
        """)
        cfg = load_config(nav=nav_cfg, site_url='http://example.com/')
        files = Files(
            [File(list(item.values())[0], cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls'])
             for item in nav_cfg]
        )
        site_navigation = get_navigation(files, cfg)
        self.assertEqual(str(site_navigation).strip(), expected)
        self.assertEqual(len(site_navigation.items), 2)
        self.assertEqual(len(site_navigation.pages), 2)
        self.assertEqual(repr(site_navigation.homepage), "Page(title='Home', url='/')")

    def test_nav_no_directory_urls(self):
        nav_cfg = [
            {'Home': 'index.md'},
            {'About': 'about.md'}
        ]
        expected = dedent("""
        Page(title='Home', url='/index.html')
        Page(title='About', url='/about.html')
        """)
        cfg = load_config(nav=nav_cfg, use_directory_urls=False, site_url='http://example.com/')
        files = Files(
            [File(list(item.values())[0], cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls'])
             for item in nav_cfg]
        )
        site_navigation = get_navigation(files, cfg)
        self.assertEqual(str(site_navigation).strip(), expected)
        self.assertEqual(len(site_navigation.items), 2)
        self.assertEqual(len(site_navigation.pages), 2)

    def test_nav_missing_page(self):
        nav_cfg = [
            {'Home': 'index.md'}
        ]
        expected = dedent("""
        Page(title='Home', url='/')
        """)
        cfg = load_config(nav=nav_cfg, site_url='http://example.com/')
        files = Files([
            File('index.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']),
            File('page_not_in_nav.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls'])
        ])
        site_navigation = get_navigation(files, cfg)
        self.assertEqual(str(site_navigation).strip(), expected)
        self.assertEqual(len(site_navigation.items), 1)
        self.assertEqual(len(site_navigation.pages), 1)
        for file in files:
            self.assertIsInstance(file.page, Page)

    def test_nav_no_title(self):
        nav_cfg = [
            'index.md',
            {'About': 'about.md'}
        ]
        expected = dedent("""
        Page(title=[blank], url='/')
        Page(title='About', url='/about/')
        """)
        cfg = load_config(nav=nav_cfg, site_url='http://example.com/')
        files = Files([
            File(nav_cfg[0], cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']),
            File(nav_cfg[1]['About'], cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls'])
        ])
        site_navigation = get_navigation(files, cfg)
        self.assertEqual(str(site_navigation).strip(), expected)
        self.assertEqual(len(site_navigation.items), 2)
        self.assertEqual(len(site_navigation.pages), 2)

    def test_nav_external_links(self):
        nav_cfg = [
            {'Home': 'index.md'},
            {'Local': '/local.html'},
            {'External': 'http://example.com/external.html'}
        ]
        expected = dedent("""
        Page(title='Home', url='/')
        Link(title='Local', url='/local.html')
        Link(title='External', url='http://example.com/external.html')
        """)
        cfg = load_config(nav=nav_cfg, site_url='http://example.com/')
        files = Files([File('index.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls'])])
        with self.assertLogs('mkdocs', level='DEBUG') as cm:
            site_navigation = get_navigation(files, cfg)
        self.assertEqual(
            cm.output,
            [
                "DEBUG:mkdocs.structure.nav:An absolute path to '/local.html' is included in the "
                "'nav' configuration, which presumably points to an external resource.",
                "DEBUG:mkdocs.structure.nav:An external link to 'http://example.com/external.html' "
                "is included in the 'nav' configuration."
            ]
        )
        self.assertEqual(str(site_navigation).strip(), expected)
        self.assertEqual(len(site_navigation.items), 3)
        self.assertEqual(len(site_navigation.pages), 1)

    def test_nav_bad_links(self):
        nav_cfg = [
            {'Home': 'index.md'},
            {'Missing': 'missing.html'},
            {'Bad External': 'example.com'}
        ]
        expected = dedent("""
        Page(title='Home', url='/')
        Link(title='Missing', url='missing.html')
        Link(title='Bad External', url='example.com')
        """)
        cfg = load_config(nav=nav_cfg, site_url='http://example.com/')
        files = Files([File('index.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls'])])
        with self.assertLogs('mkdocs', level='WARNING') as cm:
            site_navigation = get_navigation(files, cfg)
        self.assertEqual(
            cm.output,
            [
                "WARNING:mkdocs.structure.nav:A relative path to 'missing.html' is included "
                "in the 'nav' configuration, which is not found in the documentation files",
                "WARNING:mkdocs.structure.nav:A relative path to 'example.com' is included "
                "in the 'nav' configuration, which is not found in the documentation files"
            ]
        )
        self.assertEqual(str(site_navigation).strip(), expected)
        self.assertEqual(len(site_navigation.items), 3)
        self.assertEqual(len(site_navigation.pages), 1)

    def test_indented_nav(self):
        nav_cfg = [
            {'Home': 'index.md'},
            {'API Guide': [
                {'Running': 'api-guide/running.md'},
                {'Testing': 'api-guide/testing.md'},
                {'Debugging': 'api-guide/debugging.md'},
                {'Advanced': [
                    {'Part 1': 'api-guide/advanced/part-1.md'},
                ]},
            ]},
            {'About': [
                {'Release notes': 'about/release-notes.md'},
                {'License': '/license.html'}
            ]},
            {'External': 'https://example.com/'}
        ]
        expected = dedent("""
        Page(title='Home', url='/')
        Section(title='API Guide')
            Page(title='Running', url='/api-guide/running/')
            Page(title='Testing', url='/api-guide/testing/')
            Page(title='Debugging', url='/api-guide/debugging/')
            Section(title='Advanced')
                Page(title='Part 1', url='/api-guide/advanced/part-1/')
        Section(title='About')
            Page(title='Release notes', url='/about/release-notes/')
            Link(title='License', url='/license.html')
        Link(title='External', url='https://example.com/')
        """)
        cfg = load_config(nav=nav_cfg, site_url='http://example.com/')
        files = Files([
            File('index.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']),
            File('api-guide/running.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']),
            File('api-guide/testing.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']),
            File('api-guide/debugging.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']),
            File('api-guide/advanced/part-1.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']),
            File('about/release-notes.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']),
        ])
        site_navigation = get_navigation(files, cfg)
        self.assertEqual(str(site_navigation).strip(), expected)
        self.assertEqual(len(site_navigation.items), 4)
        self.assertEqual(len(site_navigation.pages), 6)
        self.assertEqual(repr(site_navigation.homepage), "Page(title='Home', url='/')")
        self.assertIsNone(site_navigation.items[0].parent)
        self.assertEqual(site_navigation.items[0].ancestors, [])
        self.assertIsNone(site_navigation.items[1].parent)
        self.assertEqual(site_navigation.items[1].ancestors, [])
        self.assertEqual(len(site_navigation.items[1].children), 4)
        self.assertEqual(repr(site_navigation.items[1].children[0].parent), "Section(title='API Guide')")
        self.assertEqual(site_navigation.items[1].children[0].ancestors, [site_navigation.items[1]])
        self.assertEqual(repr(site_navigation.items[1].children[1].parent), "Section(title='API Guide')")
        self.assertEqual(site_navigation.items[1].children[1].ancestors, [site_navigation.items[1]])
        self.assertEqual(repr(site_navigation.items[1].children[2].parent), "Section(title='API Guide')")
        self.assertEqual(site_navigation.items[1].children[2].ancestors, [site_navigation.items[1]])
        self.assertEqual(repr(site_navigation.items[1].children[3].parent), "Section(title='API Guide')")
        self.assertEqual(site_navigation.items[1].children[3].ancestors, [site_navigation.items[1]])
        self.assertEqual(len(site_navigation.items[1].children[3].children), 1)
        self.assertEqual(repr(site_navigation.items[1].children[3].children[0].parent), "Section(title='Advanced')")
        self.assertEqual(site_navigation.items[1].children[3].children[0].ancestors,
                         [site_navigation.items[1].children[3], site_navigation.items[1]])
        self.assertIsNone(site_navigation.items[2].parent)
        self.assertEqual(len(site_navigation.items[2].children), 2)
        self.assertEqual(repr(site_navigation.items[2].children[0].parent), "Section(title='About')")
        self.assertEqual(site_navigation.items[2].children[0].ancestors, [site_navigation.items[2]])
        self.assertEqual(repr(site_navigation.items[2].children[1].parent), "Section(title='About')")
        self.assertEqual(site_navigation.items[2].children[1].ancestors, [site_navigation.items[2]])
        self.assertIsNone(site_navigation.items[3].parent)
        self.assertEqual(site_navigation.items[3].ancestors, [])
        self.assertIsNone(site_navigation.items[3].children)

    def test_nested_ungrouped_nav(self):
        nav_cfg = [
            {'Home': 'index.md'},
            {'Contact': 'about/contact.md'},
            {'License Title': 'about/sub/license.md'},
        ]
        expected = dedent("""
        Page(title='Home', url='/')
        Page(title='Contact', url='/about/contact/')
        Page(title='License Title', url='/about/sub/license/')
        """)
        cfg = load_config(nav=nav_cfg, site_url='http://example.com/')
        files = Files(
            [File(list(item.values())[0], cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls'])
             for item in nav_cfg]
        )
        site_navigation = get_navigation(files, cfg)
        self.assertEqual(str(site_navigation).strip(), expected)
        self.assertEqual(len(site_navigation.items), 3)
        self.assertEqual(len(site_navigation.pages), 3)

    def test_nested_ungrouped_nav_no_titles(self):
        nav_cfg = [
            'index.md',
            'about/contact.md',
            'about/sub/license.md'
        ]
        expected = dedent("""
        Page(title=[blank], url='/')
        Page(title=[blank], url='/about/contact/')
        Page(title=[blank], url='/about/sub/license/')
        """)

        cfg = load_config(nav=nav_cfg, site_url='http://example.com/')
        files = Files(
            [File(item, cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']) for item in nav_cfg]
        )
        site_navigation = get_navigation(files, cfg)
        self.assertEqual(str(site_navigation).strip(), expected)
        self.assertEqual(len(site_navigation.items), 3)
        self.assertEqual(len(site_navigation.pages), 3)
        self.assertEqual(repr(site_navigation.homepage), "Page(title=[blank], url='/')")

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_nested_ungrouped_no_titles_windows(self):
        nav_cfg = [
            'index.md',
            'about\\contact.md',
            'about\\sub\\license.md',
        ]
        expected = dedent("""
        Page(title=[blank], url='/')
        Page(title=[blank], url='/about/contact/')
        Page(title=[blank], url='/about/sub/license/')
        """)

        cfg = load_config(nav=nav_cfg, site_url='http://example.com/')
        files = Files(
            [File(item, cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']) for item in nav_cfg]
        )
        site_navigation = get_navigation(files, cfg)
        self.assertEqual(str(site_navigation).strip(), expected)
        self.assertEqual(len(site_navigation.items), 3)
        self.assertEqual(len(site_navigation.pages), 3)

    def test_nav_from_files(self):
        expected = dedent("""
        Page(title=[blank], url='/')
        Page(title=[blank], url='/about/')
        """)
        cfg = load_config(site_url='http://example.com/')
        files = Files([
            File('index.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']),
            File('about.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls'])
        ])
        site_navigation = get_navigation(files, cfg)
        self.assertEqual(str(site_navigation).strip(), expected)
        self.assertEqual(len(site_navigation.items), 2)
        self.assertEqual(len(site_navigation.pages), 2)
        self.assertEqual(repr(site_navigation.homepage), "Page(title=[blank], url='/')")

    def test_nav_from_nested_files(self):
        expected = dedent("""
        Page(title=[blank], url='/')
        Section(title='About')
            Page(title=[blank], url='/about/license/')
            Page(title=[blank], url='/about/release-notes/')
        Section(title='Api guide')
            Page(title=[blank], url='/api-guide/debugging/')
            Page(title=[blank], url='/api-guide/running/')
            Page(title=[blank], url='/api-guide/testing/')
            Section(title='Advanced')
                Page(title=[blank], url='/api-guide/advanced/part-1/')
        """)
        cfg = load_config(site_url='http://example.com/')
        files = Files([
            File('index.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']),
            File('about/license.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']),
            File('about/release-notes.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']),
            File('api-guide/debugging.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']),
            File('api-guide/running.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']),
            File('api-guide/testing.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']),
            File('api-guide/advanced/part-1.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']),
        ])
        site_navigation = get_navigation(files, cfg)
        self.assertEqual(str(site_navigation).strip(), expected)
        self.assertEqual(len(site_navigation.items), 3)
        self.assertEqual(len(site_navigation.pages), 7)
        self.assertEqual(repr(site_navigation.homepage), "Page(title=[blank], url='/')")

    def test_active(self):
        nav_cfg = [
            {'Home': 'index.md'},
            {'API Guide': [
                {'Running': 'api-guide/running.md'},
                {'Testing': 'api-guide/testing.md'},
                {'Debugging': 'api-guide/debugging.md'},
                {'Advanced': [
                    {'Part 1': 'api-guide/advanced/part-1.md'},
                ]},
            ]},
            {'About': [
                {'Release notes': 'about/release-notes.md'},
                {'License': 'about/license.md'}
            ]}
        ]
        cfg = load_config(nav=nav_cfg, site_url='http://example.com/')
        files = Files([
            File('index.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']),
            File('api-guide/running.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']),
            File('api-guide/testing.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']),
            File('api-guide/debugging.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']),
            File('api-guide/advanced/part-1.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']),
            File('about/release-notes.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']),
            File('about/license.md', cfg['docs_dir'], cfg['site_dir'], cfg['use_directory_urls']),
        ])
        site_navigation = get_navigation(files, cfg)
        # Confirm nothing is active
        self.assertTrue(all(page.active is False for page in site_navigation.pages))
        self.assertTrue(all(item.active is False for item in site_navigation.items))
        # Activate
        site_navigation.items[1].children[3].children[0].active = True
        # Confirm ancestors are activated
        self.assertTrue(site_navigation.items[1].children[3].children[0].active)
        self.assertTrue(site_navigation.items[1].children[3].active)
        self.assertTrue(site_navigation.items[1].active)
        # Confirm non-ancestors are not activated
        self.assertFalse(site_navigation.items[0].active)
        self.assertFalse(site_navigation.items[1].children[0].active)
        self.assertFalse(site_navigation.items[1].children[1].active)
        self.assertFalse(site_navigation.items[1].children[2].active)
        self.assertFalse(site_navigation.items[2].active)
        self.assertFalse(site_navigation.items[2].children[0].active)
        self.assertFalse(site_navigation.items[2].children[1].active)
        # Deactivate
        site_navigation.items[1].children[3].children[0].active = False
        # Confirm ancestors are deactivated
        self.assertFalse(site_navigation.items[1].children[3].children[0].active)
        self.assertFalse(site_navigation.items[1].children[3].active)
        self.assertFalse(site_navigation.items[1].active)