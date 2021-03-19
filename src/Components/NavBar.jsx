const NavBar = () => {
  return (
    <div id="navbar">
      <div className="navbar-item">
        <p>The University</p>
      </div>
      <div className="navbar-item" id="navbar-button-holder">
        {logoutButton}
      </div>
    </div>
  );
};

export default NavBar;
