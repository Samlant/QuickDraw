var __index = {"config":{"lang":["en"],"separator":"[\\s\\-]+","pipeline":["stopWordFilter"]},"docs":[{"location":"features.html","title":"Features","text":""},{"location":"features.html#program-features","title":"Program Features:","text":"<ul> <li>leverages a daemon/background service to automatically detect new client quoteforms</li> <li>creates a custom/complete folder structure for the client</li> <li>differentiates between new business and renewals</li> <li>allocate markets for a client and this will include them in the tracker</li> <li>send a fully automated---yet customizable---submission via email into underwriters representing 9 different programs</li> <li>gets, saves, &amp; handles updating user authentication automatically after first execution</li> </ul>"},{"location":"features.html#flexibility-that-it-offers-you","title":"Flexibility that it offers you:","text":"<ul> <li>easy-to-INSTALL, USE, &amp; CUSTOMIZE</li> <li> <p>set defaults for various portions of the email, including:</p> </li> <li> <p>attachments,</p> </li> <li>email addresses (to, cc),</li> <li>greeting / intro / body elements</li> <li>salutation / name / signature image</li> <li> <p>limited custom HTML for styling;</p> </li> <li> <p>handles multiple markets that use the same email address---cough MPG</p> </li> <li> <p>customize the message for any combination</p> </li> <li> <p>all defaults are provided, ready to submit as-is</p> </li> <li> <p>simple install process and clean uninstall</p> </li> </ul>"},{"location":"features.html#updates-from-previous-release-v250-alpha","title":"Updates from previous release (v2.5.0-alpha):","text":"<ul> <li>utilizes MS Graph API rather than desktop Office applications, including authentication-handling and request-making</li> <li>automatic trigger via a background/daemon service</li> <li>automatic dir creation</li> <li>automatic client tracking in excel report</li> <li>displays an interactive sys tray icon</li> <li>refined internal structure and design</li> <li>less coupling between modules and greater cohesion within them</li> </ul>"},{"location":"install.html","title":"Installation Details","text":"<p>After running setup.exe, the program installs itself to your user's folder</p> <pre><code>C:\\Users\\your_user_name\\AppData\\Local\\Worktools\n</code></pre> <p>as well as make a startmenu shortcut, desktop shortcut and adds itself to the boot-up sequence.</p> <p>You may access the program from</p> <ul> <li>the system tray icon in the lower-right corner</li> <li>the StartMenu in the lower-left corner (or Windows key)</li> <li>Desktop icon</li> </ul>"},{"location":"license.html","title":"License","text":""},{"location":"license.html#mit-license","title":"MIT License","text":"<p>Copyright (c) 2023 Samuel Alexander Lanteigne</p> <p>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the \"Software\"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</p> <p>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</p> <p>THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</p>"},{"location":"readme.html","title":"Overview","text":"<p> Note: You may run this Readme either in Light Mode or Dark Mode, by pressing the sun near the search bar in the top-right corner.</p>"},{"location":"readme.html#overview","title":"Overview","text":"<p>A customizable, automated client intake tool to organize your new clients on your system, track them via an excel tracker, &amp; boasts a powerful email submission tool to submit quote requests to several markets for you---easily &amp; efficiently..</p> <p></p> <p>QuickDraw is a program that utilizes Microsoft's Graph API for:</p> <ul> <li>reading/writing files (including a report tracker)</li> <li>sending emails through Outlook</li> </ul>"},{"location":"readme.html#base-concept","title":"Base Concept","text":"<p>Recall a time that you just got off the phone with a client after taking their information and you were immediately interrupted with another phone call, only soon to find yourself distracted long enough to miss a step in your refined routine...</p> <pre><code>ie. making an entry to keep track of them and their quotes\n</code></pre> <p>... so the new client remains in the shadows long enough to eventually create a panic situation...</p> <ol> <li>This will watch a specified folder for any new, saved quoteforms;<ul> <li>can be customized to any folder or set of folders (just let me know);</li> </ul> </li> <li>creates a custom/complete folder hierarchy for the client;</li> <li>Client details are prefilled automatically and used throughout the program, which removes much of the manual effort from your end;</li> <li>Do you already know which markets are a good fit for this client? Allocate markets and this will include those markets within your tracker;</li> <li>Ready for submission? This will use a customizable template to submit your quoteform into nine different programs;<ul> <li>add any/all attachments you want by simply clicking and dragging the files;</li> <li>Note: default templates are provided for each program, so it's ready to submit as-is;</li> </ul> </li> <li>Review the submission and finalize with any extra/last-minute notes or adjustments</li> <li>Send your submissions quickly, cleanly create folders for your clients, and ensure all clients are tracked---even if you don't immediately send to UW or know which markets to send to.</li> </ol> <p> Note: You can use the auto-emailing program anytime by right-clicking the system tray icon in the lower-right of your computer</p> System Tray Icon"},{"location":"readme.html#license","title":"License","text":"<p>For more info on the license, see the License page</p>"},{"location":"readme.html#authors","title":"Authors","text":"<ul> <li>@Samlant</li> </ul>"},{"location":"roadmap.html","title":"Roadmap","text":"<p>Legend:</p> Icon Definition = Haven't started = Work in Progress = Finished = Stretch Goal <p> Am always refactoring &amp; abstracting code in new ways to improve flexibility, robustness, customizability, and lessen code-dependency;</p> <p> Further refine modules' layouts and content;</p> <p> Further refine documentation for end-users, as well as for internal methods/classes;</p> <p> Implement validation methods;</p> <p> Include the needed quoteforms (for the drag-n-drop functionality) in the repo;</p> <p> Automate moving 6-month old &amp; older quotes to an archive folder;</p> <p> Allow customization of additional elements, like the subject line, &amp; HTML styling;</p> <p> Alow user to edit the folders that get auto-created;vff</p> <p> Automate Surplus Lines documentation (stamping, etc.);</p> <p> Update GUI when able (PyQT6/5 or Kivy);</p> <p> Send emails using outlook account;</p> <p> Include specific quote details in subject line (name, boat);</p> <p> Allow users to include any last-minute notes into body of the email message;</p> <p> Incorporate extensible CC functionality;</p> <p> Automate the process by clicking &amp; dragging a quoteform to attach to email, rather than manually typing;</p> <p> Allow other attachments to be included within the email;</p> <p> Allow users to define most aspects of the email content by creating a customizations tab for templates;</p> <p> Settings should be capable to be saved across sessions (persistent); create a config file as it's most-suitable;</p> <p> Refine field names in the quoteform;</p> <p> Establish a workflow to feed data from quote intake ==&gt; submissions to markets;</p> <p> Auto-populate an entry into our excell tracking report;</p> <p> Combine with my IntakeTool (monitor for new clients);</p> <p> Create an installer to install the program into user's AppData\\Local folder;</p>"},{"location":"support.html","title":"Support","text":"<p>For support or if you have any feedback, send us an email at sam@novamar.net</p>"},{"location":"support.html#faq","title":"FAQ","text":""},{"location":"support.html#i-cant-view-my-emails-before-sending-or-view-an-example-of-a-template","title":"I can't view my emails before sending or view an example of a template?","text":"<p>Viewing emails or templates is currently not supported yet. For toubleshooting, feel free to set your email address as the To: address to see a working version of your current template.</p>"},{"location":"support.html#how-can-i-edit-my-signature-or-the-subject-line","title":"How can I edit my signature, or the subject line?","text":"<p>Currently, there are only options to edit your salutation, name, and picture of your signature(if desired); there isn't an method to access other attributes of the signature (or subject line)---such as HTML styling, the business address, disclosures or locations. While the program covers most of the essentials, in the near future as the program matures, we will be implementing more customizations to you as the user. If any special requests need to be made, contact us below under Support and we'll try to accommodate your request.</p>"},{"location":"quickstart/configurations-options.html","title":"Customization Options","text":""},{"location":"quickstart/configurations-options.html#customize-templates","title":"Customize Templates","text":"<p>You may edit any of these by selecting the drop-down box and selecting a market.</p> <p> Some of those options represent occurences where multiple markets submit to the same email address: you can edit all combinations so that you have all your bases covered regarding templates.</p> <p> Viewing emails or current examples is not currently supported yet.</p> <p></p>"},{"location":"quickstart/configurations-options.html#customize-cc-and-signature","title":"Customize CC and Signature","text":"<p>To change the signature image (in your case, it's replacing the digitized signature), you may either click-and-drag an image onto the box or browse for a file.</p> <p> an unlimited number of CC addresses can be put on either line; both lines get combined.</p> <p></p>"},{"location":"quickstart/quickstart.html","title":"Quick-Start","text":""},{"location":"quickstart/quickstart.html#running-the-program","title":"Running the Program","text":"<p>By default, the program runs upon start-up.</p> <p>To confirm this, you should see this icon in the lower right-corner of your screen:</p> <p></p> <pre><code>You may need to click the upwards-arrow to expand the icons shown\n</code></pre> <p></p> <p>As the program runs, it monitors a specified folder for any new client quoteforms.</p> <p>Once it detects a new one saved, it will open a dialog window for you to decide what to do with the quoteform. options inlcude:</p> <ol> <li>Move the quoteform to the folder where you keep other quoteforms and create an entry in an excel tracking report (all of this is automated)---also creates any additional folders that you'd like according to your organization preferences;</li> <li>Same as #1, plus select which markets you would like to eventually submit to for this client (these markets will show up on your tracker)</li> <li>Same as #1, plus launch another window for you to quickly send the quoteform out to any programs/carriers that you'd like to.</li> </ol> <p>With Option #3, you have the followding customizations:</p> <ul> <li>CC any number of people;</li> <li>add last-minute notes fdfdto the email body;</li> <li>extensively modify the outgoing email messages on a per-carrier basis;</li> <li>attach any additional attachments</li> </ul> <p>If you would like to use this program to email submissions to underwriters at a later time:</p> <p>simply right-click the binoculars icon in the lower-right corner of your screen and select \"Run QuickDraw\".</p> <ul> <li>This will launch the main program window;</li> <li>See Submitting to Markets for how to use this window in-depth.</li> </ul>"},{"location":"quickstart/quickstart.html#authenticate-your-account-for-the-first-time","title":"Authenticate Your Account for the First Time","text":"<p>Once you send emails for the first time, Microsoft will ask you to login. This is to authenticate you so that you're authorized to send emails from your account \"name@novamar.net\"</p> <p></p> <p>Once you enter your username &amp; password, on the next screen you may see a rquest to approve the login. If you have enabled 2nd Factor Authentication on your Microsoft account, you will see this:</p> <p></p> <p>Depending on your settings, to confirm you may be able to:</p> <ul> <li>Use the Microsoft Authenticator App on phone/tablet/watch</li> <li>confirm an email</li> <li>confirm a text message</li> </ul> <p>After the first time of doing this, the program re-authenticates itself automatically before the current permission expires.</p> <p> You will not need to do this again.</p>"},{"location":"quickstart/quickstart.html#you-dont-have-to-stay-signed-in","title":"You Don't Have to Stay Signed-in","text":"<p>After approving your login, if you see this screen, you do NOT have to stay signed in; it's a new browser session every time.</p> <p></p>"},{"location":"quickstart/submitting.html","title":"Submitting to Markets","text":"<p>The main window of the program is shown below:</p> <p></p>"},{"location":"quickstart/submitting.html#quoteform","title":"Quoteform","text":"<p> Note that if this program was triggered automatically from a new quoteform and you chose to submit to markets, the client's quoteform will already be attached and shown in the top-left-most box.</p> <p>Otherwise, simply left-click-and-drag the quoteform onto the top-left box. Once you release the mouse button, the name of the quoteform should be shown in the box, which most likely represents the client's name (parsed from the PDF file).</p> <p>You may now left-click-and-drag any other files that you would like to send underwriters (boating resumes, surveys, vessel/dock photos, etc.) onto the lower-left box.</p> <p> If you click-and-drag another quoteform---or any other file---onto this top-left box, it will delete the former and replace it with the latter. Be aware of this.</p>"},{"location":"quickstart/submitting.html#select-markets","title":"Select Markets","text":"<ul> <li> <p>On the right-side, select which markets that you would like to send your client into.</p> </li> <li> <p>More will be added upon request, just let me know.</p> </li> </ul>"},{"location":"quickstart/submitting.html#last-minute-adjustments","title":"Last-minute Adjustments","text":""},{"location":"quickstart/submitting.html#quick-items-to-note","title":"Quick items to note:","text":"<p> Note: these submissions are sent with pre-existing email templates, so extra notes are not necessary for most submissions.</p> <p> Note also: Additionally, there are also email addresses that are \"CC'd\" by default...</p> <pre><code>**cough** file@novamar.net\n</code></pre> <p>If you wish to edit the templates or default CC addresses---or to know more about them---please see Configurations Options</p>"},{"location":"quickstart/submitting.html#however","title":"However,","text":"<p>In combination with the customizable templates, you may want to add last-minute notes within the email body, or include other people on the CC for a particular submission---which leads us to the next couple sections...</p>"},{"location":"quickstart/submitting.html#extra-notes","title":"Extra Notes","text":"<ul> <li>You can enter any extra notes/text within the center-top box and it will be included in the email body, lastly but right before your salutation;</li> </ul>"},{"location":"quickstart/submitting.html#modify-cc-addresses","title":"Modify \"CC\" addresses","text":"<ul> <li>Within the center-bottom section of the window, you can input any additional addresses that you'd like to CC on the outgoing submission</li> <li>If the checkbox is selected, the default \"CC\" addresses will be used in addition to any that you specify here;</li> <li>If the checkbox is not selected, then only the addresses specified here will be copied on the outgoing emails;</li> </ul> <p> Note: an unlimited number of addresses can be put here.</p> <p> Please separate the emails using a semi-colon \";\".</p>"}]}