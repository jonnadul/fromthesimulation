---
layout: post
title: "Charting the Developer World"
subtitle: "A simple project to map the social aspect of Github."
date: 2014-09-03 12:00:00
published: true
---
![]({{ '/assets/img/raw/1_EBspffrBD4pXdcxg53HpNg.png' | relative_url }})

*A simple project to map the social aspect of Github.*

[Github](https://www.github.com) recently hosted a [data challenge](https://github.com/blog/1864-third-annual-github-data-challenge), the premise of which was to use their exposed [APIs](https://developer.github.com/v3/) to do something interesting. At first I was just curious in the level of access they exposed, which btw is very expansive, but then I stumbled across an idea. I was interesting in capturing and visualizing the social interconnections which binded Github in a very fundamental way.

### Overview

#### Functionality

![]({{ '/assets/img/raw/1_a4uAo54cvV2XsrDkydHNXQ.png' | relative_url }})

*Screencap of Github-map*

The application basically takes in a Github username, queries all public facing repositories of that user, queries all the watchers of each repository, and generates a node-link tree mapping these relationships.

#### Software Layout

![]({{ '/assets/img/raw/1_1UYj3INbdr7IluWYAmMvKg.png' | relative_url }})

The front-end is drive by [AngularJS](https://angularjs.org/), a very popular MVC framework, with visualizations being handled by [D](http://d3js.org/)3. The back-end is driven by [NodeJS](http://nodejs.org/), which handles queries to Github APIs, using [node-github](https://github.com/mikedeboer/node-github). Query results are handled as JSON objects and exchanged to the front-end via REST, [see](http://scotch.io/tutorials/javascript/build-a-restful-api-using-node-and-express-4).

### Github API Query

Using [node-github](https://github.com/mikedeboer/node-github), which wraps most of the raw APIs into nicely organized functions, for the back-end code querying code was relatively simple. Due to the event driven nature, I ended up having to use [promises](https://www.promisejs.org/) (and some hacky-coding lol) to maintain a certain level of procedural flow.

- **github.repo.getFromUser()**: Returns all repositories for a github username.
- **github.repos.getWatchers()**: Returns all watchers for a github repository.
*See, *[*server.js*](https://github.com/jonnadul/github-map/blob/master/server.js).

NOTE: As you read on to the next section, the data to that is to be visualized needed to be in a certain JSON format. You’ll notice that the back-end code is aware of this format and maintains this structure as it handles responses from Github queries.

### Data Visualization

Since I was using [AngularJS](https://angularjs.org/) as the front-end solution, it only made sense to incorporate the D3 engine within that framework as well. We do this by writing a custom [directive](https://docs.angularjs.org/guide/directive).

#### Dependency Injection

Before going about doing this, we want to setup the actual D3 dependency so it can be injected into the custom directive. This will be residing within an angular [factory](https://docs.angularjs.org/guide/providers).

```
angular.module('d3', [])
.factory('d3Service', ['$document', '$window', '$q', '$rootScope',
	function($document, $window, $q, $rootScope) {
 		var d = $q.defer(),
 	d3service = {
 		d3: function() { return d.promise; }
 	};
 	function onScriptLoad() {
 		// Load client in the browser
 		$rootScope.$apply(function() { d.resolve($window.d3); });
 	}
 	var scriptTag = $document[0].createElement('script');
 	scriptTag.type = 'text/javascript'; 
 	scriptTag.async = true;
 	scriptTag.src = 'http://d3js.org/d3.v3.min.js';
 	scriptTag.onreadystatechange = function () {
 		if (this.readyState == 'complete') onScriptLoad();
 	}
 	scriptTag.onload = onScriptLoad;
 
 	var s = $document[0].getElementsByTagName('body')[0];
 	s.appendChild(scriptTag);
 
 	return d3service;
}]);
```

#### D3 Custom Directive

Now we are ready to write the D3 custom directive.

Below is a template for how the D3 directive could look like, with the core D3 code residing within the $timeout() function. The rest of the wrapping code is intended to handle the changes in data (and the viewing environment) that affect the rendering.

```
ghmapApp.directive('d3Bars', ['$window', '$timeout', 'd3Service',
	function($window, $timeout, d3Service) {
		return {
 			restrict: 'A',
 			scope: {
 		data: '=',
 		label: '@',
 		onClick: '&'
 		},
	link: function(scope, ele, attrs) {
		d3Service.d3().then(function(d3) {
 
 	var renderTimeout;
	var svg = d3.select(ele[0])
		.append("svg");
 
 	$window.onresize = function() {
 		scope.$apply();
 	};
 
 	scope.$watch(function() {
 		return angular.element($window)[0].innerWidth;
 	}, function() {
 		scope.render(scope.data);
 	});
 
 	scope.$watch('data', function(newData) {
 		scope.render(newData);
 	}, true);
 
 	scope.render = function(data) {
 		svg.selectAll('*').remove();
 
 		if (!data) return;
			if (renderTimeout) clearTimeout(renderTimeout);
	 
			renderTimeout = $timeout(function() {
 				/*Write your D3.js code here*/
 	};
	});
	}}
}]);
```

The benefit to this template is that it added a dynamic element to the visualization rendering process. For a more in-depth explanation check out this [post](http://www.ng-newsletter.com/posts/d3-on-angular.html). One important note is to set the overarching *d3.select(ele[0])*, this will keep your animation within the bounds of the DOM element from which the directive is called.

Now its as simple as adding the following line into your *.html page.

```
<div d3-bars align="center" data="data"></div>
```

For my app I used the D3 and CSS code snippets from [Radial Reingold–Tilford Tree](http://bl.ocks.org/mbostock/4063550), by [mbostock](http://bl.ocks.org/mbostock), as my core D3 code to generated my node-link tree visual.

*See, *[*core.js*](https://github.com/jonnadul/github-map/blob/master/public/core.js)* and *[*index.html*](https://github.com/jonnadul/github-map/blob/master/public/index.html)*.*

NOTE: Check out following [book](https://leanpub.com/d3angularjs), it provides deep insight into the real power of utilizing D3 and Angular to make super lean and dynamic web apps.

And that's its! Outside of a few interesting corner cases, most of the software pieces feel into place very nicely! Please check out my project [here](https://github.com/jonnadul/github-map), and constructive feedback is always appreciated ☺.
