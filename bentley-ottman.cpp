#include <CGAL/Cartesian.h>
#include <CGAL/MP_Float.h>
#include <CGAL/Quotient.h>
#include <CGAL/Arr_segment_traits_2.h>
#include <CGAL/Sweep_line_2_algorithms.h>
#include <list>
#include <array>

#define npoints 20000
#define s0 290797
#define module 50515093

typedef CGAL::Quotient<CGAL::MP_Float>                  NT;
typedef CGAL::Cartesian<NT>                             Kernel;
typedef Kernel::Point_2                                 Point_2;
typedef CGAL::Arr_segment_traits_2<Kernel>              Traits_2;
typedef Traits_2::Curve_2                               Segment_2;



int main()
{
    long sn1, tn;
    long sn = s0;
    sn1 = (sn * sn) % module;
    sn = sn1;
    
    std::array<int, 20000> ps;
    
    for (int c = 0; c <= npoints; c++) {
        sn1 = (sn * sn) % module;
        ps[c] = (sn % 500);
        sn = sn1;
        //std::cout << "Coord " << ps.back() << std::endl; 
    }
    
    // Construct the input segments.
    //Segment_2 segments[] = {Segment_2 (Point_2 (1, 5), Point_2 (8, 5)),
    //                  Segment_2 (Point_2 (1, 1), Point_2 (8, 8)),
    //                  Segment_2 (Point_2 (3, 1), Point_2 (3, 8)),
    //                  Segment_2 (Point_2 (8, 5), Point_2 (8, 8))};

    Segment_2 * segments = new Segment_2[npoints/4] ;
    int segcounter=0;
    for (int c = 0; c <= (npoints - 4); c += 4) {
        segments[segcounter] = Segment_2 (Point_2 (ps[c], ps[c+1]), 
                Point_2 (ps[c+2], ps[c+3]));
        std::cout << "Segment " << segcounter << " " << segments[segcounter] << std::endl; 
        segcounter++;
    }

    // Compute all intersection points.
    std::list<Point_2>     pts;

    std::cout << "Found " << pts.size() << " intersection points: " << std::endl; 
    CGAL::compute_intersection_points (segments, segments + 5000,
                                 std::back_inserter (pts));

    // Print the result.
    std::cout << "Found " << pts.size() << " intersection points: " << std::endl; 
    std::copy (pts.begin(), pts.end(),
         std::ostream_iterator<Point_2>(std::cout, "\n"));

    CGAL_assertion (CGAL::do_curves_intersect (segments, segments + 4));

    delete segments;
    return 0;
}
