angular
    .module('landingPage')
    .component('landingPage', {
        controller: function (allOrgs, recentChlamPubLinks, euroPubData) {
            var ctrl = this;
            ctrl.myInterval = 5000;
            ctrl.noWrapSlides = false;
            ctrl.active = 0;
            var currIndex = 0;
            //ctrl.orgList = allChlamOrgs.getAllOrgs();
            ctrl.orgList = allOrgs.getAllOrgs();

        },
        templateUrl: '/static/wiki/js/angular_templates/landing-page.html'
    });


