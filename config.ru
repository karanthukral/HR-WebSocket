require './app'
require './middlewares/hr_backend'

use HRDemo::HRBackend

run HRDemo::App
