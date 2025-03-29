from fastapi_filter.contrib.sqlalchemy import Filter
from fastapi_filter import FilterDepends, with_prefix

from app.vacancy.models import Location, LocationBase, VacancyBase, Vacancy

class LocationSave(LocationBase):
    def to_entity(self):
        return Location(
            country=self.country,
            region=self.region,
            city=self.city
        )
        
class LocationPublic(LocationBase):
    id: str
    
    @staticmethod
    def init_scheme(location: Location):
        location_id = location.id.hex
        country = location.country
        region = location.region
        city = location.city
        return LocationPublic(
            id=location_id,
            country=country,
            region=region,
            city=city
        )

class VacancySave(VacancyBase):
    location: LocationSave
    def to_entity(self):
        return Vacancy(
            name=self.name,
            description=self.description,
            url=self.url,
        )
    

class VacancyPublic(VacancyBase):
    id: str
    location: LocationPublic
    location_id: str
    
    @staticmethod
    def init_scheme(vacancy: Vacancy):
        vacancy_id = vacancy.id.hex
        location_id = vacancy.location_id.hex
        location = LocationPublic.init_scheme(vacancy.location)
        description = vacancy.description
        name = vacancy.name
        url = vacancy.url
        return VacancyPublic(
            id=vacancy_id,
            name=name,
            description=description,
            url=url,
            location_id=location_id,
            location=location
        )
 


class LocationFilter(Filter):
    id: str | None = None
    country: str | None = None
    region: str | None = None
    city: str | None = None
    
    class Constants(Filter.Constants):
        model = Location 
        
        
class VacancyFilter(Filter):
    id: str | None = None
    location: LocationFilter | None = FilterDepends(with_prefix("location", LocationFilter))
    
    class Constants(Filter.Constants):
        model = Vacancy