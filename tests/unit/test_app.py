# """Unit test for app functions (without Flask)."""


# import pytest
# from werkzeug.exceptions import NotFound
# from flask import Request
# from advent_of_code.app import (
#     handle_exception,
#     handle_root_path,
#     handle_solve_path,
#     handle_solve_path_with_part,
#     handle_year_path,
#     request,
# )
# from advent_of_code.utils.solver_status import implementation_status


# def test_handle_root_path() -> None:
#     dates = [date for date, status in implementation_status().items() if status]

#     body, status = handle_root_path()
#     assert status == 200

#     expected_body = {
#         "years": [
#             {"year": year, "days": [x.day for x in dates if x.year == year]}
#             for year in {x.year for x in dates}
#         ]
#     }
#     assert body == expected_body


# def test_handle_year_path():
#     dates = [date for date, status in implementation_status().items() if status]

#     # test with valid year
#     body, status = handle_year_path(2015)
#     assert status == 200
#     assert body == {"year": 2015, "days": [x.day for x in dates if x.year == 2015]}

#     # test with invalid year
#     with pytest.raises(NotFound) as e:
#         handle_year_path(2100)
#     assert e.value.code == 404


# def test_handle_solver_path(year: int, day: int) -> None:
#     # test with unimplemented solver
#     with pytest.raises(NotFound) as e:
#         handle_solve_path(2014, 1)
#     assert e.value.code == 404

