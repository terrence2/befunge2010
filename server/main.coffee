###
# Copyright 2011, Terrence Cole
# 
# This file is part of Befunge2012.
# 
# Befunge2012 is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Befunge2012 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with Befunge2012.  If not, see <http://www.gnu.org/licenses/>.
###


get '/': ->
	render 'index'

view index: ->

layout ->
	html ->
		head ->
			title "Befunge2012"
			meta charset: 'utf-8'
			link rel: 'stylesheet', href: "/css/ui-darkness/jquery-ui-1.8.14.custom.css"
			style '''
			body {padding: 0px; margin: 0px;}
			'''
			script src: "/js/jquery-1.6.2.min.js"
			script src: "/js/jquery-ui-1.8.14.custom.min.js"
			coffeescript ->
				$().ready ->
					$("#run.menu").button().click ->
						b12.evaluate $("#entry").val()
					$("#clear.menu").button().click ->
						alert "clear"

		body ->
			textarea id:"entry", rows:25, cols:80, ->
				"Hello"

			div id:"menu", ->
				div id:"run", 'class':'menu', ->
					"Run"

				div id:"clear", 'class':'menu', ->
					"Clear"



