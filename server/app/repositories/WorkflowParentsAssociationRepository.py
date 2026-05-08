from types import SimpleNamespace

from ..database.connection import database
from ..models.WorkflowParentsAssociationModel import WorkflowParentsAssociationModel
from ..services.validateWorkflowParent import validateWorkflowParent


def create(workflowId, parentTypeKey, parentId):
    # ! raise error when find any issue
    validateWorkflowParent(parentTypeKey, parentId)

    # *** The "parentTypeKey" is a dynamic key for this association table
    # *** once it will have just two of the three possible collumns filled
    newAssociationParameterDict = {
        "workflowId": workflowId,
        parentTypeKey: parentId
    }
    newAssociation = WorkflowParentsAssociationModel(
        # *** This "**" operator unpacks the dictionary,
        # *** so it can be used as the constructor parameter
        **newAssociationParameterDict
    )

    database.session.add(newAssociation)
    database.session.commit()

    return newAssociation.getAttributes()

# todo: def updateParent(): ## shall move the workflow beetwen lines or projects


workflowParentsAssociationRepository = SimpleNamespace(
    create=create,
)
