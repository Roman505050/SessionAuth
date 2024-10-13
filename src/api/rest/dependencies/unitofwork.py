from fastapi import Depends
from typing import Annotated

from infrastructure.utils.unitofwork import IUnitOfWork
from infrastructure.utils.unitofwork import UnitOfWork


def get_unit_of_work() -> IUnitOfWork:
    return UnitOfWork()


UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
