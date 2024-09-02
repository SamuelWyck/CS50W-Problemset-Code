### Distinctiveness and Complexity
For my final project I created a portfolio website which I plan to deploy to the web. As such, it is completely distinct from all the other projects in this course. My website's purpose is to display the relevant information about my portfolio and to direct the user to any other relevant sites. Hence, the user intention with this site is to see the information displayed on the site and not to alter it, like one would with the wiki project for example.

For complexity, the two main features that my site displays are the coding projects I have completed, and the relevant courses I have completed. My website handles embedding videos, images, links, and the relevant text for each. The data for both my projects and courses are kept in a sqlite database structured with two django models named "project" and "course" respectively. The backend of my site collects the relevant data for each view and sends that data to the corresponding html template, which is then built out using jinja. Since there is no reason for any user but me to add data to the site, the only way to add a new project or course to the site is through the django admin interface. However, the site is modular so adding a new project or course is as simple as filling out all the fields and letting the site do the rest.

The javascript for my website is used mainly to hide unneeded links on the navbar. I also used it to add an onclick handler to each of the project cards on the index page to make into them a clickable link.



### Each file's contents


#### main app structure
My django project, named portfolio, contains a single app called projects. Inside the settings.py file I added a MEDIA_URL and a MEDIA_ROOT (called media which is a folder I added to the root folder). In addition to the logic I added in the project's urls.py file, These changes allowed me to store videos or images for my site if needed.


#### models.py
This file contains the two models I created for this app. Both models stored some type of media be that a picture or video. At first I planned to store all the images and videos natively, but I realized it would be better to allow for "offsite hosting" of the media. So I uploaded all the videos to youtube and used an embed link instead. I did the same for the images using a website called imgur.  

The "Project" model contains fields for all the info I wanted to store for each coding project.
Title: A char field to store the name of the project.
Description: A char field to store my explanation of the project.
Thumbnail: A char field that stores an embed link for an image stored on imgur.
Video: A char field that stores an embed link for a video stored on youtube.
Code_link: A char field that stores a link to a github repository that stores all the relevant code for that project.

The "Course" model contains fields for all the info I wanted to store for each course I have completed.
Title: A char field to store the name of the course.
Description: A char field to store the course description found on the course website.
Code_link:  A char field that stores a link to a github repository that stores all the relevant code for that course.
Course_link: A char field that stores a link to the courses website.


#### admin.py
In this file I registered both the Project and Course models so that I could edit, delete, and add model objects in the django admin interface.


#### urls.py
This file contains three urls I made for my app. Each one calls on a view in the views.py file.


#### views.py
This file contains the views for my app.

The "index" view is the default view for my website. When called on, it selects all the project objects from the Project model and renders the index.html template with the list of project objects as an argument.

The "project_page" view is called on when a user clicks on one of the project cards in the default view. This view gets the project object based on the project_id given to it on call. It returns a render of the project_page.html template with the project object passed as an argument.

The "courses" view is called on when a user clicks the "My Courses" link on the navbar. This view gets all the course objects from the Course model and returns a render of the courses.html template with the list of course objects passed as an argument.


#### layout.html
This file contains the base layout for my html content. In the head tag it links to the bootstrap css file and contains a meta tag for mobile responsiveness. It also has a "title block" which allows all other templates that extend it to customize the page title. There is also a "script block" which allows all other templates that extend it to add a script.

In the body tag there is a div containing the website heading. Below that, there is a navbar which has a sticky-top attribute. Lastly, there is a "body block" which allows all other templates that extend it to add content to the body of the page.


#### index.html
This file is the default template for my website. It extends the layout.html template. In the "title block" it adds its own title, and in the "script block" it adds its own .js file. In the "body block" it takes the list of project objects passed to it by the index view, and generates a card for each project object.


#### project_page.html
This file is the template for each project page for my website. It takes a project object given to it from the project_page view. It extends the layout.html template, and in the "title block" it adds the title of the project object it was given. In the "body block" it builds out a page using the info in the project object it was given. It displays the title, embeds the project's video, and builds a card containing the project's description and relevant links.


#### courses.html
This file is the template for the list of courses that I display on my website. It extends the layout.html template. In the "title block" it adds its own title, and in the "script block" it adds its own .js file. In the "body block" it takes the list of course objects passed to it by the courses view and builds a card for each course using the relevant info for each.


#### index.js
This file contains the javascript that the index.html template uses. First, it selects all the project cards on the page and then adds an onclick handler that directs the user to that project's page when a card is clicked. Second, it hides the "My Projects" link on the navbar since the website is currently at that page.


#### courses.js
This file contains the javascript that the courses.html template uses. This file simply hides the "My Courses" link on the navbar since my website is currently on that page.



### How to run application
In the root folder, run the command "python manage.py runserver" in the terminal.