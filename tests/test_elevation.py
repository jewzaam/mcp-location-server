"""
Unit tests for elevation functionality.
"""

import asyncio
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx

from mcp_location_server.elevation import OpenTopoDataElevationService
from mcp_location_server.models import ElevationRequest, ElevationData
from mcp_location_server.server import LocationServer


class TestOpenTopoDataElevationService:
    """Test the elevation service."""
    
    @pytest.fixture
    def elevation_service(self):
        """Create an elevation service for testing."""
        return OpenTopoDataElevationService()
    
    @pytest.fixture
    def sample_api_response(self):
        """Sample response from Open Topo Data API."""
        return {
            "results": [
                {
                    "dataset": "srtm90m",
                    "elevation": 124.0,
                    "location": {
                        "lat": 35.6893514,
                        "lng": -78.7767045
                    }
                }
            ],
            "status": "OK"
        }
    
    @pytest.mark.asyncio
    async def test_meters_to_feet_conversion(self, elevation_service):
        """Test meters to feet conversion."""
        assert elevation_service._meters_to_feet(100.0) == pytest.approx(328.084, rel=1e-3)
        assert elevation_service._meters_to_feet(0.0) == 0.0
        assert elevation_service._meters_to_feet(124.0) == pytest.approx(406.824, rel=1e-3)
    
    @pytest.mark.asyncio
    async def test_get_elevation_success(self, elevation_service, sample_api_response):
        """Test successful elevation request."""
        request = ElevationRequest(
            latitude=35.6893514,
            longitude=-78.7767045,
            dataset="srtm90m"
        )
        
        # Mock the HTTP client
        with patch.object(elevation_service.client, 'get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = sample_api_response
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            response = await elevation_service.get_elevation(request)
            
            assert response.count == 1
            assert len(response.results) == 1
            
            result = response.results[0]
            assert result.latitude == 35.6893514
            assert result.longitude == -78.7767045
            assert result.elevation.meters == 124.0
            assert result.elevation.feet == pytest.approx(406.824, rel=1e-3)
            assert result.elevation.dataset == "srtm90m"
    
    @pytest.mark.asyncio
    async def test_get_elevation_api_error(self, elevation_service):
        """Test elevation request with API error."""
        request = ElevationRequest(
            latitude=35.6893514,
            longitude=-78.7767045,
            dataset="srtm90m"
        )
        
        error_response = {
            "status": "INVALID_REQUEST",
            "error": "Invalid dataset"
        }
        
        with patch.object(elevation_service.client, 'get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = error_response
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            with pytest.raises(ValueError, match="Elevation API error"):
                await elevation_service.get_elevation(request)
    
    @pytest.mark.asyncio
    async def test_get_elevation_http_error(self, elevation_service):
        """Test elevation request with HTTP error."""
        request = ElevationRequest(
            latitude=35.6893514,
            longitude=-78.7767045,
            dataset="srtm90m"
        )
        
        with patch.object(elevation_service.client, 'get') as mock_get:
            mock_get.side_effect = httpx.HTTPError("Connection failed")
            
            with pytest.raises(httpx.HTTPError, match="Failed to get elevation"):
                await elevation_service.get_elevation(request)
    
    @pytest.mark.asyncio
    async def test_get_elevation_no_results(self, elevation_service):
        """Test elevation request with no results."""
        request = ElevationRequest(
            latitude=35.6893514,
            longitude=-78.7767045,
            dataset="srtm90m"
        )
        
        empty_response = {
            "results": [],
            "status": "OK"
        }
        
        with patch.object(elevation_service.client, 'get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = empty_response
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            response = await elevation_service.get_elevation(request)
            
            assert response.count == 0
            assert len(response.results) == 0
    
    @pytest.mark.asyncio
    async def test_get_elevation_simple_success(self, elevation_service, sample_api_response):
        """Test simple elevation lookup."""
        with patch.object(elevation_service.client, 'get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = sample_api_response
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            elevation_data = await elevation_service.get_elevation_simple(
                35.6893514, -78.7767045, "srtm90m"
            )
            
            assert elevation_data is not None
            assert elevation_data.meters == 124.0
            assert elevation_data.feet == pytest.approx(406.824, rel=1e-3)
            assert elevation_data.dataset == "srtm90m"
    
    @pytest.mark.asyncio
    async def test_get_elevation_simple_error(self, elevation_service):
        """Test simple elevation lookup with error."""
        with patch.object(elevation_service.client, 'get') as mock_get:
            mock_get.side_effect = httpx.HTTPError("Connection failed")
            
            elevation_data = await elevation_service.get_elevation_simple(
                35.6893514, -78.7767045, "srtm90m"
            )
            
            assert elevation_data is None


class TestLocationServerElevation:
    """Test elevation functionality in LocationServer."""
    
    @pytest.fixture
    def location_server(self):
        """Create a LocationServer for testing."""
        return LocationServer()
    
    @pytest.mark.asyncio
    async def test_get_elevation_success(self, location_server):
        """Test successful elevation lookup via LocationServer."""
        sample_elevation_data = ElevationData(
            meters=124.0,
            feet=406.824,
            dataset="srtm90m"
        )
        
        with patch('mcp_location_server.server.get_elevation_service') as mock_get_service:
            mock_service = AsyncMock()
            mock_response = MagicMock()
            mock_response.results = [MagicMock()]
            mock_response.results[0].latitude = 35.6893514
            mock_response.results[0].longitude = -78.7767045
            mock_response.results[0].elevation = sample_elevation_data
            
            mock_service.get_elevation.return_value = mock_response
            mock_get_service.return_value = mock_service
            
            result = await location_server.get_elevation(35.6893514, -78.7767045, "srtm90m")
            
            assert result["found"] is True
            assert result["latitude"] == 35.6893514
            assert result["longitude"] == -78.7767045
            assert result["elevation_meters"] == 124.0
            assert result["elevation_feet"] == pytest.approx(406.824, rel=1e-3)
            assert result["dataset"] == "srtm90m"
    
    @pytest.mark.asyncio
    async def test_get_elevation_no_data(self, location_server):
        """Test elevation lookup with no data available."""
        with patch('mcp_location_server.server.get_elevation_service') as mock_get_service:
            mock_service = AsyncMock()
            mock_response = MagicMock()
            mock_response.results = []
            
            mock_service.get_elevation.return_value = mock_response
            mock_get_service.return_value = mock_service
            
            result = await location_server.get_elevation(35.6893514, -78.7767045, "srtm90m")
            
            assert result["found"] is False
            assert result["latitude"] == 35.6893514
            assert result["longitude"] == -78.7767045
            assert result["elevation_meters"] is None
            assert result["elevation_feet"] is None
            assert result["dataset"] == "srtm90m"
            assert "message" in result
    
    @pytest.mark.asyncio
    async def test_get_elevation_validation_error(self, location_server):
        """Test elevation lookup with invalid coordinates."""
        result = await location_server.get_elevation(999.0, -78.7767045, "srtm90m")
        
        assert result["found"] is False
        assert "error" in result
        assert result["error"] == "Invalid request"
    
    @pytest.mark.asyncio
    async def test_get_elevation_http_error(self, location_server):
        """Test elevation lookup with HTTP error."""
        with patch('mcp_location_server.server.get_elevation_service') as mock_get_service:
            mock_service = AsyncMock()
            mock_service.get_elevation.side_effect = httpx.HTTPError("Connection failed")
            mock_get_service.return_value = mock_service
            
            result = await location_server.get_elevation(35.6893514, -78.7767045, "srtm90m")
            
            assert result["found"] is False
            assert "error" in result
            assert result["error"] == "API request failed"


class TestElevationModels:
    """Test elevation data models."""
    
    def test_elevation_request_valid(self):
        """Test valid elevation request."""
        request = ElevationRequest(
            latitude=35.6893514,
            longitude=-78.7767045,
            dataset="srtm90m"
        )
        
        assert request.latitude == 35.6893514
        assert request.longitude == -78.7767045
        assert request.dataset == "srtm90m"
    
    def test_elevation_request_invalid_latitude(self):
        """Test elevation request with invalid latitude."""
        with pytest.raises(Exception):
            ElevationRequest(
                latitude=999.0,  # Invalid latitude
                longitude=-78.7767045,
                dataset="srtm90m"
            )
    
    def test_elevation_request_invalid_longitude(self):
        """Test elevation request with invalid longitude."""
        with pytest.raises(Exception):
            ElevationRequest(
                latitude=35.6893514,
                longitude=999.0,  # Invalid longitude
                dataset="srtm90m"
            )
    
    def test_elevation_data_conversion(self):
        """Test elevation data with unit conversion."""
        elevation_data = ElevationData(
            meters=100.0,
            feet=328.084,
            dataset="srtm90m"
        )
        
        assert elevation_data.meters == 100.0
        assert elevation_data.feet == pytest.approx(328.084, rel=1e-3)
        assert elevation_data.dataset == "srtm90m"