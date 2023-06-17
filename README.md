# QuickDraw

### A mass-email-sender that sequentially submits quotes to various markets for you easily & efficiently.

![Logo](https://i.postimg.cc/CK3Gbr4Z/6-DB2-F6-EE-F692-4-EDD-A987-9-FBE2999355-A.png)

This quick application is a tool that allows you to:

1. Drag a quoteform, along with any attachments, onto the window;

2. Select which markets to submit for a quote;

3. Sends individual emails to all desired markets---each with their own unique message;

4. Allows you, the user, to customize those email messages to a large degree;

5. It also has the ability to CC people (1) on a one-time basis, (2) by default, and/or, (3) both.

## License

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

## Authors

- [@Samlant](https://github.com/Samlant)

## Features

| :black_small_square: | Feature List                                                                                                                                                                                                                                                                                                               |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| :clinking_glasses:   | Sends emails using your Outlook account without needing credentials or any passwords passed to it, yet does not have any admin access granted to it.                                                                                                                                                                       |
| :clinking_glasses:   | Every email is unique based on persistent templates saved in a config file.                                                                                                                                                                                                                                                |
| :clinking_glasses:   | This config file is user-friendly & very readable, enough for anyone to be able to edit it---most times without frustration; give it a looksie.                                                                                                                                                                            |
| :clinking_glasses:   | The CarbonCopy (CC) features can accommodate an unlimited number of CC's both in the config file & on the user-interface; just separate them with ";" as you normally would in Outlook.                                                                                                                                    |
| :clinking_glasses:   | Likewise, you may also attach any number of attachments to accommodate your quote request, such as captain's license, resume, survey, etc.                                                                                                                                                                                 |
| :clinking_glasses:   | Incorporates a professionally-legible Novamar-branded signature, inclusive of links to company's website & social media.                                                                                                                                                                                                   |
| :clinking_glasses:   | Gathering details about the submission is performed automatically by extracting data from the QuoteForm PDF.                                                                                                                                                                                                               |
| :clinking_glasses:   | For example, the subject line will contain client's first & last name, details of the vessel, & an identifier that the email is for a quote request.                                                                                                                                                                       |
| :clinking_glasses:   | Forgot to include something in the quoteform or want to drop a quick note to underwriting just for this client? You may easily add any last-minute notes that will be included within the body of the email in a logical progression---no matter how you start or end---this should be improved by AI when incorporated... |

## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)

## FAQ

#### No emails are sent when I press either the "send" or "view" buttons, what can I do?

> Make sure that you have Outlook open & running first before running the program. If that doesn't work, send us an email. Note that we require Outlook to be running so that no passwords are collected for this to work---privacy first!

#### How can I edit my signature, or the subject line?

> Currently, there are only options to edit your salutation, name, and picture of your signature(if desired); there isn't an method to access other attributes of the signature (or subject line)---such as HTML styling, the business address, disclosures or locations. While the program covers most of the essentials, in the near future as the program matures, we will be implementing more customizations to you as the user. If any special requests need to be made, contact us below under Support and we'll try to accommodate your request.

## Roadmap

#### Legend:

| Icon                 | Definition       |
| -------------------- | ---------------- |
| :mailbox_with_mail:  | Haven't started  |
| :rowing_man: =       | Work in Progress |
| :heavy_check_mark: = | Finished         |
| :muscle: =           | Stretch Goal     |

:rowing_man: \*Always extracting and abstracting code to improve flexibility and robustness in new ways.

:rowing_man: Establish a workflow to feed data from quote intake ==> submissions to markets

:rowing_man: Auto-populate an entry into our excell tracking report

:rowing_man: Clean-up modules' layouts and content & compose/refine complete documentation of modules/methods.

:mailbox_with_mail: Implement validation methods.

:mailbox_with_mail: Create an installer to install the program into user's AppData\Local folder.

:mailbox_with_mail: Include the needed quoteform (for the drag-n-drop functionality) in the repo.

:mailbox_with_mail: Refine field names in the quoteform.

:muscle: Allow customization of additional elements, like the subject line & HTML styling.

:muscle: Update GUI to PyQT6 when able.

:muscle: Combine with my other suite of office productivity tools

:heavy_check_mark: Send emails using outlook account

:heavy_check_mark: Include specific quote details in subject line (name, boat)

:heavy_check_mark: Allow users to include any last-minute notes into body of the email message.

:heavy_check_mark: Incorporate extensible CC functionality.

:heavy_check_mark: Automate the process by clicking & dragging a quoteform to attach to email, rather than manually typing.

:heavy_check_mark: Allow other attachments to be included within the email.

:heavy_check_mark: Allow users to define most aspects of the email content by creating a customizations tab for templates.

:heavy_check_mark: Settings should be capable to be saved across sessions (persistent); create a config file as it's most-suitable.

## Support

For support or if you have any feedback, email either sam@wildernessexplorers.us or nat@wildernessexplorers.us

## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.

Please adhere to this project's `code of conduct`.

## Related

Here are some related projects to this one:

[Placeholder_for_other_helpful_script](https://github.com/matiassingers/awesome-readme)
