import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Menu,
  MenuItem,
  Container,
  Paper,
} from "@mui/material";

const Dashboard = () => {
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const handleMenuClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div style={{ backgroundColor: "#f5f5f5", minHeight: "100vh" }}>
      {/* Navbar */}
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" style={{ flexGrow: 1 }}>
            Dashboard
          </Typography>
          <Button color="inherit" onClick={handleMenuClick}>
            Account
          </Button>
          <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleMenuClose}>
            <MenuItem onClick={() => { navigate("/update-settings"); handleMenuClose(); }}>
              Update Settings
            </MenuItem>
            <MenuItem onClick={() => { navigate("/"); handleMenuClose(); }}>
              Home Page
            </MenuItem>
            <MenuItem onClick={() => { handleLogout(); handleMenuClose(); }}>
              Sign Out
            </MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>

      {/* Main Content */}
      <Container>
        <Paper elevation={3} style={{ padding: "20px", marginTop: "50px", textAlign: "center" }}>
          <Typography variant="h5" color="textPrimary">
            Welcome to your Dashboard!
          </Typography>
          <Typography variant="body1" color="textSecondary" style={{ marginTop: "10px" }}>
            Here you can update your settings and manage your account.
          </Typography>
        </Paper>
      </Container>
    </div>
  );
};

export default Dashboard;
