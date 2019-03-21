//import { vue } from "../src/main.js"
//import { app } from "../src/App.vue"
import axios from "axios";
import Login from "../src/pages/Login.vue";
import VeeValidate from "vee-validate";
//import router from "../src/router"

import { mount, createLocalVue } from "@vue/test-utils";

const localVue = createLocalVue();
localVue.use(VeeValidate);
var sinon = require('sinon');

describe("Login.vue", () => {
    it("testing Login page renders", () => {
        var wrapper = mount(Login, { localVue, sync: false });

        var message = wrapper.find(".login__banner").text();

        expect(message).toBe("Admin");
    })

    it("testing Login page validation", () => {
        var loginSpy = sinon.spy(Login.methods, "loginUser");
        var wrapper = mount(Login, { localVue, sync: false });

        var resolved = new Promise((r) => r({ data: [] }));
        var post = sinon.stub(axios, "post").returns(resolved);

        wrapper.vm.email = "test@test.com";
        wrapper.vm.password = "password";
        wrapper.find("button").trigger("click");

        sinon.assert.calledOnce(loginSpy);

        post.restore();
        loginSpy.restore();
    })
})
