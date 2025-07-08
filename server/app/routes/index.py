from flask import Blueprint

from .suFilesRouter import suFileRouter
from .suFilePathRouter import suFilePathRouter
from .userRouter import userRouter
from .sessionRouter import sessionRouter

from .projectRouter import projectRouter
from .lineRouter import lineRouter
from .workflowRouter import workflowRouter
from .commandRouter import commandRouter

from .datasetRouter import datasetRouter

from .admin.programRouter import programRouter
from .admin.programGroupRouter import programGroupRouter
from .admin.parameterRouter import parameterRouter

router = Blueprint("routes", __name__)

router.register_blueprint(suFileRouter)
router.register_blueprint(suFilePathRouter)
router.register_blueprint(userRouter)
router.register_blueprint(sessionRouter)

router.register_blueprint(projectRouter)
router.register_blueprint(lineRouter)
router.register_blueprint(workflowRouter)
router.register_blueprint(commandRouter)

router.register_blueprint(datasetRouter)

# *** Admin based Routes ***
router.register_blueprint(programRouter)
router.register_blueprint(programGroupRouter)
router.register_blueprint(parameterRouter)
