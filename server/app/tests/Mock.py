import pytest
from os import path

DEFAULT_PASSWORD = "password123"


class Mock():
    client = pytest.client
    base_marmousi_stack_path = path.join(
        path.dirname(__file__),
        "mock_seismic_data",
        "marmousi_4ms_stack.su"
    )
    user = dict()
    project = dict()
    line = dict()
    workflow = dict()
    # *** valid sufilter command
    sufilterCommand = dict()
    created_file_link = dict()

    programGroup = dict()
    program = dict()
    token: str = ""

    def loadUser(self, name="root"):
        email = f'{name}@email.com'
        response = self.client.post(
            "/user/create",
            json={
                "name": name,
                "email": email,
                "password": DEFAULT_PASSWORD
            }
        )
        user_data = response.json
        self.user = user_data
        return user_data

    def loadSession(self, email=None, password=DEFAULT_PASSWORD):
        response = self.client.post(
            "/session/",
            json={
                "email": email or self.user["email"],
                "password": password
            }
        )

    def loadProject(self):
        response = self.client.post(
            "/project/create",
            json={
                "name": "project_test",
                "userId": self.user["id"],
            },
        )
        project_data = response.json
        self.project = project_data
        return project_data

    def loadLine(self):
        response = self.client.post(
            f"/line/create/{self.project['id']}",
            json={
                "name": "line_test",
                "projectId": self.project["id"],
            },
        )
        line_data = response.json
        self.line = line_data
        return line_data

    def loadWorkflow(self):
        response = self.client.post(
            f"/workflow/create/{self.project['id']}",
            json={
                "name": "workflow_test",
                "parentType": "projectId"
            },
        )
        workflow_data = response.json
        self.workflow = workflow_data
        return workflow_data

    def loadProgramGroup(self):
        response = self.client.post(
            f"/programs/groups/create",
            json={
                "name": "program_test",
                "description": "no description"
            },
        )
        programGroupData = response.json
        self.programGroup = programGroupData
        return programGroupData

    def loadProgram(
        self,
        name="program_test",
        description="no description",
    ):
        response = self.client.post(
            f"/programs/create/{self.programGroup['id']}",
            data={
                "name": name,
                "description": description,
                "path_to_executable_file": name,
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            }
        )
        programData = response.json
        self.program = programData
        return programData

    def loadSufilterCommand(self):
        # *** load valid sufilter program
        # *** load valid command with valid paremeters for sufilter
        self.loadProgram(
            name="sufilter",
            description="applies a zero-phase, sine-squared tapered filter"
        )
        parameters = {
            "f": "10, 20, 150, 200",
            "amps": "0, 1, 1, 0"
        }
        response = self.client.post(
            f"/dataset/create/{self.workflow['id']}",
            json={
                "name": "sufilter",
                "parameters": parameters,
                "program_id": self.program['id'],
            },
        )
        commandData = response.json
        self.sufilterCommand = commandData
        return commandData

    def loadSuFileLink(self):
        with open(self.base_marmousi_stack_path, "rb") as file:
            response = self.client.post(
                f"/su-file/create/{self.workflow['id']}",
                data={
                    "file": (file, path.basename(file.name))
                },
                content_type="multipart/form-data",
            )

            created_file_link = response.json['fileLink']
            self.created_file_link = created_file_link
            return created_file_link

    def linkSuFileInputToWorkflow(self):
        self.client.put(
            f"/workflow/update/{self.workflow['id']}/file",
            json={
                "fileLinkId": self.created_file_link["id"],
            },
        )
