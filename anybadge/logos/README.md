# Bundled logos

The SVG files in this directory are logos bundled with the `anybadge`
package, so badges using them can be generated offline and without any
network access. They are used when a badge logo is given as a Simple
Icons-style name (e.g. `logo=python`), after any user-supplied
`logo_dirs` search path and before downloading from the Simple Icons
CDN.

## Adding more bundled logos

Additional logos are welcome via PR to this
[jongracecox/anybadge](https://github.com/jongracecox/anybadge)
repository. To add one:

1. Download the icon from the Simple Icons CDN as a white SVG, matching
   the convention used by the existing files (white matches this
   package's default badge text color):

   ```
   https://cdn.simpleicons.org/<slug>/white
   ```

   e.g. `https://cdn.simpleicons.org/fastapi/white`

2. Save it in this directory as `<slug>.svg` (lowercase, using the
   Simple Icons slug as the file name), and make sure the file ends
   with a newline.

3. Check the icon renders sensibly on a badge, e.g.:

   ```
   anybadge --label=value --value=1 --logo=<slug> --file=test_logo.svg
   ```

4. Add the slug to the bundled logos list in the main `README.md`
   (the CLI `--logo` help lists bundled logos automatically).

Keep bundled logos limited to commonly used project logos, and prefer
reusing an existing icon over adding a near-duplicate. Larger or
unusually licensed images should instead be vendored by users via
`anybadge fetch-logos` or local files.

## Source and license

These files were obtained from [Simple Icons](https://simpleicons.org)
(`https://cdn.simpleicons.org`), released under the
[CC0 1.0 Universal](https://github.com/simple-icons/simple-icons/blob/develop/LICENSE.md)
public domain dedication. No attribution is required by the license; it
is provided here as a courtesy.

## Trademarks

All logos in this directory are trademarks of their respective brand
owners. Their inclusion here, and their rendering within anybadge
badges, does not imply any affiliation with, or endorsement by, any of
the brand owners. Users should observe the respective brand owners'
usage guidelines when using logos in their own badges.
