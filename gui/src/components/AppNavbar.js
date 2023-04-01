import Container from 'react-bootstrap/Container'
import Navbar from 'react-bootstrap/Navbar'

export default function AppNavbar() {
  return (
    <>
      <Navbar bg="dark" variant="dark">
        <Container>
          <Navbar.Brand href="#home">
            Von Neumann Machine
          </Navbar.Brand>
        </Container>
      </Navbar>
    </>
  )
}