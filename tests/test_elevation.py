"""
Unit tests for elevation functionality.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from mcp_location_server.elevation import OpenTopoDataElevationService
from mcp_location_server.models import ElevationData, ElevationRequest
from mcp_location_server.server import LocationServer

# Test constants
TEST_LATITUDE = 35.6893514
TEST_LONGITUDE = -78.7767045
TEST_ELEVATION_METERS = 124.0
TEST_ELEVATION_FEET = 406.824
CONVERSION_FACTOR_100M = 100.0
CONVERSION_FACTOR_100M_FEET = 328.084
INVALID_LATITUDE = 999.0
INVALID_LONGITUDE = 999.0


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
                        "lng": -78.7767045,
                    },
                },
            ],
            "status": "OK",
        }

    @pytest.mark.asyncio
    async def test_meters_to_feet_conversion(self, elevation_service):
        """Test meters to feet conversion."""
        assert elevation_service._meters_to_feet(
            CONVERSION_FACTOR_100M,
        ) == pytest.approx(
            CONVERSION_FACTOR_100M_FEET,
            rel=1e-3,
        )
        assert elevation_service._meters_to_feet(0.0) == 0.0
        assert elevation_service._meters_to_feet(
            TEST_ELEVATION_METERS,
        ) == pytest.approx(
            TEST_ELEVATION_FEET,
            rel=1e-3,
        )

    @pytest.mark.asyncio
    async def test_get_elevation_success(self, elevation_service, sample_api_response):
        """Test successful elevation request."""
        request = ElevationRequest(
            latitude=TEST_LATITUDE,
            longitude=TEST_LONGITUDE,
            dataset="srtm90m",
        )

        # Mock the HTTP client
        with patch.object(elevation_service.client, "get") as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = sample_api_response
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            response = await elevation_service.get_elevation(request)

            assert response.count == 1
            assert len(response.results) == 1

            result = response.results[0]
            assert result.latitude == TEST_LATITUDE
            assert result.longitude == TEST_LONGITUDE
            assert result.elevation.meters == TEST_ELEVATION_METERS
            assert result.elevation.feet == pytest.approx(TEST_ELEVATION_FEET, rel=1e-3)
            assert result.elevation.dataset == "srtm90m"

    @pytest.mark.asyncio
    async def test_get_elevation_api_error(self, elevation_service):
        """Test elevation request with API error."""
        request = ElevationRequest(
            latitude=TEST_LATITUDE,
            longitude=TEST_LONGITUDE,
            dataset="srtm90m",
        )

        error_response = {
            "status": "INVALID_REQUEST",
            "error": "Invalid dataset",
        }

        with patch.object(elevation_service.client, "get") as mock_get:
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
            latitude=TEST_LATITUDE,
            longitude=TEST_LONGITUDE,
            dataset="srtm90m",
        )

        with patch.object(elevation_service.client, "get") as mock_get:
            mock_get.side_effect = httpx.HTTPError("Connection failed")

            with pytest.raises(httpx.HTTPError, match="Failed to get elevation"):
                await elevation_service.get_elevation(request)

    @pytest.mark.asyncio
    async def test_get_elevation_no_results(self, elevation_service):
        """Test elevation request with no results."""
        request = ElevationRequest(
            latitude=TEST_LATITUDE,
            longitude=TEST_LONGITUDE,
            dataset="srtm90m",
        )

        empty_response = {
            "results": [],
            "status": "OK",
        }

        with patch.object(elevation_service.client, "get") as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = empty_response
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            response = await elevation_service.get_elevation(request)

            assert response.count == 0
            assert len(response.results) == 0

    @pytest.mark.asyncio
    async def test_get_elevation_simple_success(
        self,
        elevation_service,
        sample_api_response,
    ):
        """Test simple elevation lookup."""
        with patch.object(elevation_service.client, "get") as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = sample_api_response
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            elevation_data = await elevation_service.get_elevation_simple(
                35.6893514,
                -78.7767045,
                "srtm90m",
            )

            assert elevation_data is not None
            assert elevation_data.meters == TEST_ELEVATION_METERS
            assert elevation_data.feet == pytest.approx(406.824, rel=1e-3)
            assert elevation_data.dataset == "srtm90m"

    @pytest.mark.asyncio
    async def test_get_elevation_simple_error(self, elevation_service):
        """Test simple elevation lookup with error."""
        with patch.object(elevation_service.client, "get") as mock_get:
            mock_get.side_effect = httpx.HTTPError("Connection failed")

            elevation_data = await elevation_service.get_elevation_simple(
                35.6893514,
                -78.7767045,
                "srtm90m",
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
            dataset="srtm90m",
        )

        with patch(
            "mcp_location_server.server.get_elevation_service",
        ) as mock_get_service:
            mock_service = AsyncMock()
            mock_response = MagicMock()
            mock_response.results = [MagicMock()]
            mock_response.results[0].latitude = 35.6893514
            mock_response.results[0].longitude = -78.7767045
            mock_response.results[0].elevation = sample_elevation_data

            mock_service.get_elevation.return_value = mock_response
            mock_get_service.return_value = mock_service

            result = await location_server.get_elevation(
                35.6893514,
                -78.7767045,
                "srtm90m",
            )

            assert result["found"] is True
            assert result["latitude"] == TEST_LATITUDE
            assert result["longitude"] == TEST_LONGITUDE
            assert result["elevation_meters"] == TEST_ELEVATION_METERS
            assert result["elevation_feet"] == pytest.approx(406.824, rel=1e-3)
            assert result["dataset"] == "srtm90m"

    @pytest.mark.asyncio
    async def test_get_elevation_no_data(self, location_server):
        """Test elevation lookup with no data available."""
        with patch(
            "mcp_location_server.server.get_elevation_service",
        ) as mock_get_service:
            mock_service = AsyncMock()
            mock_response = MagicMock()
            mock_response.results = []

            mock_service.get_elevation.return_value = mock_response
            mock_get_service.return_value = mock_service

            result = await location_server.get_elevation(
                35.6893514,
                -78.7767045,
                "srtm90m",
            )

            assert result["found"] is False
            assert result["latitude"] == TEST_LATITUDE
            assert result["longitude"] == TEST_LONGITUDE
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
        with patch(
            "mcp_location_server.server.get_elevation_service",
        ) as mock_get_service:
            mock_service = AsyncMock()
            mock_service.get_elevation.side_effect = httpx.HTTPError(
                "Connection failed",
            )
            mock_get_service.return_value = mock_service

            result = await location_server.get_elevation(
                35.6893514,
                -78.7767045,
                "srtm90m",
            )

            assert result["found"] is False
            assert "error" in result
            assert result["error"] == "API request failed"


class TestElevationModels:
    """Test elevation data models."""

    def test_elevation_request_valid(self):
        """Test valid elevation request."""
        request = ElevationRequest(
            latitude=TEST_LATITUDE,
            longitude=TEST_LONGITUDE,
            dataset="srtm90m",
        )

        assert request.latitude == TEST_LATITUDE
        assert request.longitude == TEST_LONGITUDE
        assert request.dataset == "srtm90m"

    def test_elevation_request_invalid_latitude(self):
        """Test elevation request with invalid latitude."""
        with pytest.raises(ValueError, match="Latitude .* between"):
            ElevationRequest(
                latitude=INVALID_LATITUDE,  # Invalid latitude
                longitude=TEST_LONGITUDE,
                dataset="srtm90m",
            )

    def test_elevation_request_invalid_longitude(self):
        """Test elevation request with invalid longitude."""
        with pytest.raises(ValueError, match="Longitude .* between"):
            ElevationRequest(
                latitude=TEST_LATITUDE,
                longitude=INVALID_LONGITUDE,  # Invalid longitude
                dataset="srtm90m",
            )

    def test_elevation_data_conversion(self):
        """Test elevation data with unit conversion."""
        elevation_data = ElevationData(
            meters=100.0,
            feet=328.084,
            dataset="srtm90m",
        )

        assert elevation_data.meters == CONVERSION_FACTOR_100M
        assert elevation_data.feet == pytest.approx(328.084, rel=1e-3)
        assert elevation_data.dataset == "srtm90m"
