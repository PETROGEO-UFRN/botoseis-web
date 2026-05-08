import { useState, useEffect } from 'react';
import { Link } from '@tanstack/react-location';

import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import TableCell from '@mui/material/TableCell';
import IconButton from '@mui/material/IconButton'

import DeleteRoundedIcon from '@mui/icons-material/DeleteRounded'

import UserMenu from 'components/UserMenu';
import { getProjectsByUser, deleteProject } from 'services/projectServices';
import NewProjectDialog from './NewProjectDialog';
import {
  Container,
  CustomHeadCell,
} from './styles'

export default function ProjectsList() {
  const [projects, setProjects] = useState<Array<IProject>>([])

  const pushNewProject = (newProject: IProject) => {
    setProjects([...projects, newProject])
  }

  const triggerDeleteButton = async (projectId: number) => {
    const responseData = await deleteProject(projectId)
    if (responseData)
      setProjects((oldProjects) => oldProjects.filter(
        (oldProject) => oldProject.id !== projectId
      ))
  }

  useEffect(() => {
    getProjectsByUser().then((result) => {
      Array.isArray(result) && setProjects(result)
    })
  }, [])

  return (
    <Container>
      <Table stickyHeader	>
        <TableHead>
          <TableRow>
            <CustomHeadCell>
              Name
            </CustomHeadCell>

            <CustomHeadCell>
              Created at
            </CustomHeadCell>

            <CustomHeadCell>
              Last modified at
            </CustomHeadCell>

            <CustomHeadCell align="right">
              <UserMenu />
            </CustomHeadCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {projects.map((project) => (
            <TableRow
              key={project.id}
              hover
            >
              <TableCell>
                <Link to={`/projects/${project.id}`}>
                  {project.name}
                </Link>
              </TableCell>

              <TableCell>
                {project.created_at}
              </TableCell>

              <TableCell>
                {project.modified_at}
              </TableCell>

              <TableCell>
                <IconButton onClick={() => triggerDeleteButton(project.id)}>
                  <DeleteRoundedIcon />
                </IconButton>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <NewProjectDialog pushNewProject={pushNewProject} />
    </Container>
  )
}
