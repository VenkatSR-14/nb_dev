import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { AppBar, Toolbar, Typography, Button, Menu, MenuItem } from "@mui/material";
import { isAuthenticated, logout } from "../utils/auth";

const Navbar = () => {
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const handleMenuClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography
          variant="h6"
          style={{ flexGrow: 1, cursor: "pointer" }}
          onClick={() => navigate("/")}
        >
          NutriBuddy
        </Typography>

        {isAuthenticated() && (
          <>
            <Button color="inherit" onClick={handleMenuClick}>
              Account
            </Button>
            <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleMenuClose}>
              <MenuItem onClick={() => { navigate("/dashboard"); handleMenuClose(); }}>
                Dashboard
              </MenuItem>
              <MenuItem onClick={() => { navigate("/update-settings"); handleMenuClose(); }}>
                Update Settings
              </MenuItem>
              <MenuItem onClick={() => { logout(); handleMenuClose(); }}>
                Sign Out
              </MenuItem>
            </Menu>
          </>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
