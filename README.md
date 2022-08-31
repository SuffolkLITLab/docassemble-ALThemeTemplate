# docassemble.ALThemeTemplate

Formerly `ALGenericJurisdiction`

Generic package that you can customize for your own state/jurisdiction's need.

It can be used to:

1. Contain shared questions, so you can standardize the way questions
are asked in your organization's interviews
1. Provide a standardized look and feel, including colors, fonts, and logos
1. Provide a custom output template for use in the Weaver, which can
control the order and contents of the generated interview YAML files

## How to use this package

Pull this package into your own playground. You should not "fork" this package using GitHub's fork button.

Edit the individual files in this repository to fit your brand's
needs.

Rename the "custom_organization.yml" file match your brand name.

Create a new Docassemble
"Package", add the files from this package, and then create a new repository on GitHub.

Install the package on your server.

Then, assuming you name the new package "MyBrand" and you renamed the "custom_organization.yml" file "my_brand.yml", in your interviews that you want to use this package's brand
and style, add an "include" line like this:

```yaml
include:
  - docassemble.MyBrand:my_brand.yml
```