"""
Plugin for UrlResolver
Copyright (C) 2020 gujal

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from __generic_resolver__ import GenericResolver

class faselhdResolver(GenericResolver):
    name = "faselhd"
    domains = ['tempb06.faseldom.xyz', 'vidfast.co']
    #pattern = r'(?://|\.)(?:faseldom|vidfast)/(?:xyz|co)?([0-9a-zA-Z]+)'