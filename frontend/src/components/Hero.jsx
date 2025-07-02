import { Link } from 'react-router-dom';
const Hero = ({
    title = 'All your grades. One smart platform.',
    subtitle = 'Track student records, progress, and performance all in one simple dashboard built for students and teachers.'
}) => {
  return (
    <section className= "bg-primary text-white text-center py-5 mt-1 mb-4">
        <div className="container">
            <h1 className="display-8">{title}</h1>
            <p className="lead-8">{subtitle}</p>
            <Link to="/add-student" className="btn btn-light btn-lg">Add Student</Link>
            <Link to="/add-student-course" className="btn btn-light btn-lg ms-2">Add Student Courses</Link>
        </div>
    </section>
  )
}

export default Hero