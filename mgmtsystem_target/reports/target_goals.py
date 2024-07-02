# -*- coding: utf-8 -*-
import base64
import io
import os
import re
import time
from datetime import datetime
from io import StringIO
from math import ceil

import lxml.html
from lxml import etree
from odoo import _, api, models
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from PIL import Image



