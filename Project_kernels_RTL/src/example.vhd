
library ieee;
use ieee.std_logic_1164.all;

entity example is
	generic (
		C_TDATA_WIDTH : integer := 512;
		C_TDEST_WIDTH : integer := 16
	);
	port (
		ap_clk : in std_logic;
    	ap_rst_n : in std_logic;
    	so_tdata : out std_logic_vector (C_TDATA_WIDTH-1 downto 0);
    	so_tvalid : out std_logic;
    	so_tready : in std_logic;
    	so_tkeep : out std_logic_vector ((C_TDATA_WIDTH/8)-1 downto 0);
    	so_tlast : out std_logic;
    	so_tdest : out std_logic_vector (C_TDEST_WIDTH-1 downto 0);
    	si_tdata : in std_logic_vector (C_TDATA_WIDTH-1 downto 0);
    	si_tvalid : in std_logic;
    	si_tready : out std_logic;
    	si_tkeep : in std_logic_vector ((C_TDATA_WIDTH/8)-1 downto 0);
    	si_tlast : in std_logic;
    	si_tdest : in std_logic_vector (C_TDEST_WIDTH-1 downto 0)
	);

end example;


architecture behavior of example is

	signal internal0_tdata, internal1_tdata : std_logic_vector (C_TDATA_WIDTH-1 downto 0);
	signal internal0_tvalid, internal1_tvalid : std_logic;
	signal internal0_tready, internal1_tready : std_logic;
	signal internal0_tkeep, internal1_tkeep : std_logic_vector ((C_TDATA_WIDTH/8)-1 downto 0);
	signal internal0_tlast, internal1_tlast : std_logic;
	signal internal0_tdest, internal1_tdest : std_logic_vector (C_TDEST_WIDTH-1 downto 0);

begin
	
	inputReg: entity work.axis_reg generic map (C_TDATA_WIDTH => C_TDATA_WIDTH, C_TDEST_WIDTH => C_TDEST_WIDTH) port map (
		ap_clk => ap_clk,
		ap_rst_n => ap_rst_n,
		x_tdata => si_tdata,
		x_tvalid => si_tvalid,
		x_tready => si_tready,
		x_tkeep => si_tkeep,
		x_tlast => si_tlast,
		x_tdest => si_tdest,
		y_tdata => internal0_tdata, 
		y_tvalid => internal0_tvalid,
		y_tready => internal0_tready,
		y_tkeep => internal0_tkeep,
		y_tlast => internal0_tlast,
		y_tdest => internal0_tdest
	);

	outputReg: entity work.axis_reg generic map (C_TDATA_WIDTH => C_TDATA_WIDTH, C_TDEST_WIDTH => C_TDEST_WIDTH) port map (
		ap_clk => ap_clk,
		ap_rst_n => ap_rst_n,
		x_tdata => internal1_tdata,
		x_tvalid => internal1_tvalid,
		x_tready => internal1_tready,
		x_tkeep => internal1_tkeep,
		x_tlast => internal1_tlast,
		x_tdest => internal1_tdest,
		y_tdata => so_tdata, 
		y_tvalid => so_tvalid,
		y_tready => so_tready,
		y_tkeep => so_tkeep,
		y_tlast => so_tlast,
		y_tdest => so_tdest
	);

	-- If you want to keep the registers, then add your code below here

	internal1_tdata <= internal0_tdata;
	internal1_tvalid <= internal0_tvalid;
	internal1_tkeep <= internal0_tkeep;
	internal1_tlast <= internal0_tlast;
	internal1_tdest <= internal0_tdest;
	internal0_tready <= internal1_tready;

end behavior;

