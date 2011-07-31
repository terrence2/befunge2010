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

GOALS = \
	build/main.js 


all: ${GOALS}
	cat ${GOALS} > public/release/befunge2012.js

watch:
	while inotifywait b12/*; do sleep 0.1; make; done

clean:
	rm -f build/*.js
	rm -f public/release/*.js

build/%.js : b12/%.coffee
	coffee -o build -b -c $<


