import {NavLink} from 'react-router-dom';
import {Navbar, Nav, Container} from 'react-bootstrap';


const NavigationBar = () => {
  return (
    <Navbar bg="primary" variant="dark" expand="lg">
      <Container fluid>{}
        <Navbar.Brand as={NavLink} to="/">Student Gradebook</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link as={NavLink} to="/" end>Home</Nav.Link>
            <Nav.Link as={NavLink} to="/add-student">Add Student</Nav.Link>
            <Nav.Link as={NavLink} to="/students">Student Records</Nav.Link>
            <Nav.Link as={NavLink} to= "/add-student-course">Add Student Courses</Nav.Link>
            <Nav.Link as={NavLink} to="/grades">Grades</Nav.Link>
            <Nav.Link as={NavLink} to="/courses">Courses</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

{/* <nav className='navbar navbar-dark bg-primary'>
        <div className='container-fluid'>
          <a className='navbar-brand' href='#'>Student Management System</a>
        </div>
      </nav> */}

export default NavigationBar