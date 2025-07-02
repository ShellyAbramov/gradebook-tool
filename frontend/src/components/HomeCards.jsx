import {Link} from 'react-router-dom';

const HomeCards = () => {
  return (
    <>
    <section className="py-5">
        <div className="container-xl">
            <div className = "row g-5 rounded showdow-sm ">
                <div className='col-12 col-md-6'>
                    <div className="card p-4">
                        <h2 className="h4 fw-bold text-center">
                            Course Enrollment Tracker
                        </h2>
                        <p className="text-center">
                            Track student course enrollments and manage their academic journey.
                        </p>
                        <Link to="/courses" className="btn btn-primary rounded w-100">
                            View Courses
                        </Link>
                    </div>
                </div>

                <div className='col-12 col-md-6'>
                    <div className="card p-4">
                        <h2 className="h4 fw-bold text-center">
                            GPA Calculator
                        </h2>
                        <p className="text-center">
                            View and calculate GPA instantly based on your course grades and credits.
                        </p>
                        <Link to="/students" className="btn btn-primary rounded w-100">
                            View GPA
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    </section>


    <section className="py-5">
        <div className="container-xl">
            <div className = "row g-5 rounded showdow-sm ">
                <div className='col-12 col-md-6'>
                    <div className="card p-4">
                        <h2 className="h4 fw-bold text-center">
                            Student Grades
                        </h2>
                        <p className="text-center">
                            View student grades and performance across all courses.
                        </p>
                        <Link to="/grades" className="btn btn-primary rounded w-100">
                            View Grades
                        </Link>
                    </div>
                </div>

                <div className='col-12 col-md-6'>
                    <div className="card p-4">
                        <h2 className="h4 fw-bold text-center">
                            Student History
                        </h2>
                        <p className="text-center">
                            Manage student history and track their academic progress over time.
                        </p>
                        <Link to="/students" className="btn btn-primary rounded w-100">
                            View Student Records
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    </section>


    </>


  )
}

export default HomeCards