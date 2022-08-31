# docassemble.ALThemeTemplate

Formerly `ALGenericJurisdiction`

Generic package that you can customize for your own state/jurisdiction's need

## How to use this package

Pull this package into your own playground. You should not "fork" this package using GitHub's fork button.

Edit the individual files in this repository to fit your brand's
needs.

Rename the "custom_organization.yml" file match your brand name.

Create a new Docassemble
"Package", add the files from this package, and then create a new repository on GitHub.

Install the package on your server.

Then, in your interviews that you want to use this package's brand
and style, add an "include" line like this:

```yaml
include:
  - docassemble.MyBrand:my_brand.yml
```