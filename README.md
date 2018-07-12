# Admin Project

This is a project that I did to learn vue.js. It uses Flask/Postgres on the backend and everything else is in Vue. It is a CRUD app.

### View Project

The project can be demoed at [my website]("https://admin.devincoty.com/").

### Model Modifications and Authentication

All model modifications made on the demo site are session based, so your modifications should have no effect on other users. Authentication has been disabled on the demo site.

### TODO

* Reports. This is partially implemented in the HomeView.vue file.
* Improvements to server-side and client-side validation. Specifically improved validation types for ids and integers/floats passed as strings.
* Query rework. Right now the serialization is on each model, which gets the job done for an app focused on Vue, but is not scalable.
* Row modifications propagate to other models besides what is in the current crud editor. Creating a new Sale ends an old one. The new Sale and all of its modifications works fine, but the old Sale needs an update in the table row, as well.
* Roles
* Forgot password and password reset
* Data structure modifications. Changes to this will need to be based off of any query modifications. Ideally, a good amount of the information will be generated on the backend in a layer between the model and response, with methods/transforms/etc. being added when passed back to the JS. It would be nice to not have to mess with long dictionary lookups and transforms on the JS side from a maintenance perspective. Some redefining of v-models should probably happen in the crud popup, as well.
* Aria/role to relevant elements
* Some "string" type fields should probably be textboxes. See: category description field
* There is still some field specific hardcoding, especially in the crud object construction and deletion detection functionality.
* A bug exists where old, but cleared, v-validate errors carry over to newly-generated Sales crud forms.
* A bug exists where the v-models of multiselects on the crud form populated from the row of a newly created object breaks the multiselects.
* Better session table implementation. The code will probably always be really hacky, but the class methods can be cleaned up and ideally there would be no need to modify the model/__init__.py. Even better if the session class models don't need to exist, either. Tracking on individual rows would also be prefered to the current method of copying tables.

### License

This project is licensed under the MIT License