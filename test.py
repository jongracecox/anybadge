#!/usr/bin/python
"""
anybadge test module.
"""

import anybadge

if __name__ == '__main__':

    thresholds={2: 'red', 4: 'orange', 6: 'green', 8: 'brightgreen'}

    badge = anybadge.Badge('test', '2.22', value_suffix='%',
                           thresholds=thresholds)

    print(badge.badge_svg_text)
