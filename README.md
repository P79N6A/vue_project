# Admin Project

This is a project that I did to learn vue.js. It uses Flask/Postgres on the backend and everything else is in Vue. It is a CRUD app.

### View Project

The project can be demoed at [my website](https://admin.devincoty.com/loading/).

### Model Modifications and Authentication

All model modifications made on the demo site are session based, so your modifications should have no effect on other users. Authentication has been disabled on the demo site.

### TODO

* Reports
* Improvements to client-side validation. VeeValidate is still causing some issues on the CRUD forms.
* Row modifications propagate to other models besides what is in the current crud editor. Creating a new Sale ends an old one. The new Sale and all of its modifications works fine, but the old Sale needs an update in the table row, as well.
* Roles
* Forgot password and password reset
* Aria/role to relevant elements
* Some "string" type fields should probably be textboxes. See: category description field
* A bug exists where old, but cleared, v-validate errors carry over to newly-generated Sales crud forms.
* A bug exists where the v-models of multiselects on the crud form populated from the row of a newly created object breaks the multiselects.
* Fix date format from server
* Fix dirty-detector on table rows
* Update CRUD to save from new format
* Finish phasing out JSON tables
* Tests to front-end
* Clean up old code
* Reimplement account popup
* Add reviews back into relevant CRUDs
* Update CSS: Specifically better support for smaller screens on the CRUD popups and the CRUD popup inputs. A general CSS pass wouldn't hurt either.
* A session strategy for the demo site that keeps the information client side, probably through Vuex.

### License

This project is licensed under the MIT License
